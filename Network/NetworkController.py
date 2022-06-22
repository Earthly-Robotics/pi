import platform
import socket
import json
import threading
import time
import RPi.GPIO as GPIO

from CameraFeed import CameraFeed
from ComponentControllers.ServoController import ServoController
from ComponentControllers.VisionController import VisionController
from Components.Camera import Camera
from Components.LoadCell import LoadCell
from Components.GyroAccelerometer import GyroAccelerometer
from Network.ConfigReader import config
from Logger.ConsoleLogger import ConsoleLogger
from Logger.FileLogger import FileLogger
from ComponentControllers.WheelsController import WheelsController


class NetworkController:
    threads = list()

    # def __init__(self, arduino_controller):
    def __init__(self, arduino_controller=None):
        match platform.system():
            case "Windows":
                self.params = config()
                self.logger = ConsoleLogger()
            case "Linux":
                self.params = config('Pi')
                self.logger = ConsoleLogger()
            case _:
                self.logger = FileLogger()
                self.logger.log("System not recognized")
        self.ip_address = self.params['ip_address']
        self.port = int(self.params['port'])
        self.buffer_size = 1000000
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_server_socket.settimeout(25)
        self.profile = 0
        self.timeout = 20
        self.limiter = 1
        self.rotate_magnet = False
        self.timeout = 600
        self.timeout_start = 0
        self.app_connected = False
        self._enabled = True

        self.arduino_controller = arduino_controller
        self.servo_controller = ServoController(arduino_controller)
        self.wheels_controller = WheelsController(self.servo_controller)
        self.app_components = self.__init_components()

    def __init_components(self):
        app_components = []
        self.load_cell = self.__start_component(LoadCell,
                                                args=(self,))
        if self.load_cell is not None:
            app_components.append(self.load_cell)

        self.accel_gyro_meter = self.__start_component(GyroAccelerometer,
                                                       args=(self,))
        if self.accel_gyro_meter is not None:
            app_components.append(self.accel_gyro_meter)

        self.camera = self.__start_component(Camera, args=(self,))
        self.vision_controller = None
        if self.camera is not None:
            app_components.append(self.camera)
            self.vision_controller = self.__start_component(VisionController,
                                                            args=(self.camera,
                                                                  self.wheels_controller,
                                                                  self))
            if self.vision_controller is not None:
                app_components.append(self.vision_controller)
                self.camera_feed = self.__start_component(CameraFeed,
                                                          args=(self,
                                                                self.vision_controller))
                if self.camera_feed is not None:
                    app_components.append(self.camera_feed)
        return app_components

    def __start_component(self, comp, args=()):
        try:
            result = comp(*args)
        except Exception as e:
            result = None
            self.logger.log("\nCould not start %s:\n%s\n" % (comp.__name__, e))
        return result

    def setup_server(self):
        """
        Starts the server
        """
        self.udp_server_socket.bind((self.ip_address, self.port))
        self.logger.log("Server online")
        self.__start_listening()

    def __start_listening(self):
        """
        Starts listening for messages on the socket.
        """
        print("Own IP: ", self.ip_address)
        print("Own Port: ", self.port)
        self.logger.log("Server started listening...")
        self.timeout_start = time.time()
        while True:
            try:
                bytes_address_pair = self.udp_server_socket.recvfrom(self.buffer_size)
            except Exception as e:
                print("Something went wrong with socket: %s " % e)
                break

            message = bytes_address_pair[0].decode()
            address = bytes_address_pair[1]
            self.client_address = address

            try:
                message = json.loads(message)
                if message is not None:
                    self.__handle_message(message)
            except json.JSONDecodeError as err:
                self.logger.log(str(err))
                bytes_to_send = str.encode("Message wasn't a JSON string")
                self.send_message(bytes_to_send, address)
        self.stop_server()

    def __handle_message(self, message):
        """
        Handles the message based on the message type.

        :param message: Received message from the socket
        """
        self.timeout_start = time.time()
        match (message["MT"]):
            case "LJ":
                x = message["x"]
                y = message["y"]
                p = message["p"]
                if self.profile != p:
                    self.profile = p
                LJ_thread = threading.Thread(target=self.wheels_controller.get_percentage, args=(x, y, self.limiter), daemon=True)
                LJ_thread.start()
            case "RJ":
                pass
                y = message["y"]
                p = message["p"]
                if self.profile != p:
                    self.profile = p
                # self.servo_controller.power_servo(y, self.profile)
            case "PB":
                pass
                p = message["p"]
                self.profile = p
            case "AB":
                if self.profile == 0:
                    self.limiter = message["l"]
                else:
                    self.rotate_magnet = not self.rotate_magnet
                    # self.servo_controller.control_magnet(self.rotate_magnet)
            case "RJB":
                pass
            case "LJB":
                pass
            case "PING":
                self.timeout_start = time.time()
                self.logger.log("Received PING.")
                if not self.app_connected:
                    for thread in self.threads:
                        if thread.name == "PING":
                            thread.join()
                    self.app_connected = True
                    self.logger.log("App connected")
                    t = threading.Thread(target=self.check_toggle_send_connection)
                    t.name = "PING"
                    self.threads.append(t)
                    t.start()
                ping = {
                    "MT": "PING"
                }
                data = json.dumps(ping)
                self.send_message(data.encode(), self.client_address)
            case "LINE_DANCE":
                pass
            case "SOLO_DANCE":
                pass
            case "PLANT":
                pass
            case "BLUE_BLOCK":
                if self.vision_controller is None:
                    self.logger.log("Can't process BLUE_BLOCK. Vision_Controller is None")
                    return
                self.vision_controller.tracking = not self.vision_controller.tracking
                self.logger.log("Received BLUE_BLOCK. Will it start sending? {0}".format(
                    self.vision_controller.tracking))
                if self.vision_controller.tracking:
                    self.camera = self.camera.start_capturing()
                else:
                    self.camera = self.camera.stop_capturing()
                self.toggle_send(sending=self.vision_controller.tracking,
                                 thread_name="BLUE_BLOCK",
                                 target=self.vision_controller.start_track_blue_cube,
                                 args=(self.client_address,)
                                 )
                block_values = self.vision_controller.get_values()
                data = json.dumps(block_values)
                self.send_message(data.encode(), self.client_address)
            case "CAMERA":
                if self.camera is None:
                    self.logger.log("Can't process CAMERA. Camera is None")
                    return
                self.camera.sending = not self.camera.sending
                self.logger.log("Received CAMERA. Will it start sending? {0}".format(
                    self.camera.sending))
                if self.camera.sending:
                    self.camera = self.camera.start_capturing()
                else:
                    self.camera = self.camera.stop_capturing()
                self.toggle_send(sending=self.camera.sending,
                                 thread_name=self.camera.msg_type,
                                 target=self.camera.update_app_data,
                                 args=(self.client_address,)
                                 )
            case "CAMERA_DEBUG":
                pass
                # if self.camera_feed is None:
                #     self.logger.log("Can't process CAMERA_DEBUG. Camera_Feed is None")
                # self.logger.log("Received CAMERA_DEBUG")
                # self.camera_feed.sending = not self.camera_feed.sending
                # self.toggle_send(sending=self.camera_feed.sending,
                #                  thread_name=self.camera_feed.msg_type,
                #                  target=self.camera_feed.update_app_data,
                #                  args=(self.client_address,))

            case "WEIGHT":
                if self.load_cell is None:
                    self.logger.log("Can't process WEIGHT. Load_cell is None")
                    return
                self.logger.log("Received WEIGHT")
                self.load_cell.sending = not self.load_cell.sending
                self.toggle_send(sending=self.load_cell.sending,
                                 thread_name=self.load_cell.msg_type,
                                 target=self.load_cell.update_app_data,
                                 args=(self.client_address,)
                                 )
            case "BLUE_BLOCK_VALUES":
                if self.vision_controller is None:
                    self.logger.log("Can't process BLUE_BLOCK_VALUES. Vision Controller is None")
                    return
                self.logger.log("Received BLUE_BLOCK_VALUES.")
                new_values = self.vision_controller.update_values(message)
                data = json.dumps(new_values)
                self.send_message(data.encode(), self.client_address)
            case "VELOCITY":
                if self.accel_gyro_meter is None:
                    self.logger.log("Can't process VELOCITY. Accel_Gyro_Meter is None")
                    return
                self.logger.log("Received VELOCITY.")
                self.accel_gyro_meter.sending = not self.accel_gyro_meter.sending
                self.toggle_send(sending=self.accel_gyro_meter.sending,
                                 thread_name=self.accel_gyro_meter.msg_type,
                                 target=self.accel_gyro_meter.update_app_data,
                                 args=(self.client_address,)
                                 )
            case "EMERGENCY_BUTTON":
                self.logger.log("EMERGENCY_BUTTON received. Stopping all components")
                self.__stop_components()
                self.app_components = self.__init_components()
                data = json.dumps({
                    "MT": "MANUAL"
                })
                self.send_message(data.encode(), self.client_address)
            case _:
                self.logger.log("{0} is not an existing MessageType".format(message["MT"]))

    def toggle_send(self, sending, thread_name, target, args=None):
        """
        Toggle continuously sending of sensor data on another thread.

        :param sending: If false, stops sending of the data and joins the thread.
        :type sending: bool
        :param thread_name: The name of the thread
        :type thread_name: str
        :param target: The target that will be run on the thread.
        :param args: The arguments for the target
        :type args: any or None
        :return:
        """
        self.timeout_start = time.time()
        if sending is False:
            for thread in self.threads:
                if thread.name == thread_name:
                    thread.join()
                    self.threads.remove(thread)

            data = json.dumps({
                "MT": "MANUAL"
            })
            self.send_message(data.encode(), self.client_address)
        else:
            if args is None:
                t = threading.Thread(target=target)
            else:
                t = threading.Thread(target=target,
                                     args=args)
            t.name = thread_name
            self.threads.append(t)
            t.start()

            data = json.dumps(self.vision_controller.get_values())
            self.send_message(data.encode(), self.client_address)
            data = json.dumps({
                "MT": thread_name
            })
            self.send_message(data.encode(), self.client_address)

    def check_toggle_send_connection(self):
        """
        Resets all the components connected to the app when the app reaches timeout.
        """
        while time.time() < self.timeout_start + self.timeout:
            time.sleep(4)
            continue
        self.logger.log("App disconnected")
        self.__stop_components()
        GPIO.cleanup()
        self.wheels_controller.reset_motors()
        self.wheels_controller = WheelsController()
        self.app_components = self.__init_components()
        self.app_connected = False

    def __stop_server(self):
        """
        Cleans up the server.
        """
        self.logger.log("Stopping the server...")
        self.timeout = 0
        self.timeout = 0
        self.app_connected = False
        self.__stop_components()

    def stop_server(self):
        self._enabled = False

    def __stop_components(self):
        """
        Stops components from sending data.
        """
        for comp in self.app_components:
            comp.stop_sending()
        for thread in self.threads:
            if thread.name == "PING":
                continue
            thread.join()
            self.threads.remove(thread)

        if self.camera is not None:
            self.camera.stop_capturing()
            self.camera.camera.release()
        self.wheels_controller.stop()

    def send_message(self, bytes_to_send, address):
        """
        Sends message to the given client

        :param bytes_to_send: The bytes that need to be sent to the client
        :type bytes_to_send: bytes
        :param address: The address that needs to receive the message
        :type address: str
        :return:
        """
        self.udp_server_socket.sendto(bytes_to_send, address)
