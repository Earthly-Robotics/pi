import asyncio
import base64
import platform
import socket
import json
import threading
import time

from ComponentControllers.VisionController import VisionController
from ComponentControllers.WheelsController import WheelsController
from Components.Camera import Camera
from Components.LoadCell import LoadCell
from Components.GyroAccelerometer import GyroAccelerometer
from Network.ConfigReader import config
from Logger.ConsoleLogger import ConsoleLogger
from Logger.FileLogger import FileLogger
from ComponentControllers.WheelsController import WheelsController
from threading import Thread


class NetworkController:
    threads = list()

    def __init__(self):
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
        self.profile = 0
        self.timeout = 600
        self.timeout_start = 0
        self.toggle_send_timeout = 600
        self.toggle_send_timeout_start = 0
        self.app_connected = False

        self.wheels_controller = WheelsController()
        self.app_components = self.__init_components()

    def __init_components(self):
        app_components = []

        self.load_cell = LoadCell(network_controller=self)
        app_components.append(self.load_cell)

        self.accel_gyro_meter = GyroAccelerometer(network_controller=self)
        app_components.append(self.accel_gyro_meter)

        self.camera = Camera(network_controller=self)
        app_components.append(self.camera)

        self.vision_controller = VisionController(cam=self.camera,
                                                  wheels_controller=self.wheels_controller,
                                                  network_controller=self)
        app_components.append(self.vision_controller)
        return app_components

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
        while time.time() < self.timeout_start + self.timeout:
            bytes_address_pair = self.udp_server_socket.recvfrom(self.buffer_size)

            message = bytes_address_pair[0].decode()
            address = bytes_address_pair[1]
            self.client_address = address

            try:
                message = json.loads(message)
                self.__handle_message(message)
            except json.JSONDecodeError as err:
                self.logger.log(str(err))
                bytes_to_send = str.encode("Message wasn't a JSON string")
                self.send_message(bytes_to_send, address)
        self.stop_server()

    def __handle_message(self, message):
        self.timeout_start = time.time()
        match (message["MT"]):
            case "LJ":
                x = message["x"]
                y = message["y"]
                p = message["p"]
                if self.profile != p:
                    self.profile = p
                LJ_thread = threading.Thread(target=self.wheels_controller.move_wheels, args=(x, y))
                LJ_thread.start()
                # self.wheels_controller.move_wheels(x, y)
                # print("LeftJoystick: x : {}, y : {}, p : {}".format(x, y, p))
            case "RJ":
                pass
                # x = message["x"]
                # y = message["y"]
                # p = message["p"]
                # if self.profile != p:
                #     self.profile = p
                # self.logger.log("RightJoystick: x : {}, y : {}".format(x, y))
                # msg_from_server = "Data RightJoystick received"
                # bytes_to_send = str.encode(msg_from_server)
                # self.send_message(bytes_to_send, self.client_address)
            case "PB":
                pass
                # p = message["p"]
                # self.profile = p
                # msg_from_server = "Profile Button received"
                # bytes_to_send = str.encode(msg_from_server)
                # self.send_message(bytes_to_send, self.client_address)
            case "VB":
                pass
            case "RJB":
                pass
            case "LJB":
                pass
            case "BATTERY":
                self.logger.log("Received BATTERY.")
            case "PING":
                self.toggle_send_timeout_start = time.time()
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
                self.vision_controller.tracking = not self.vision_controller.tracking
                self.logger.log("Received BLUE_BLOCK. Will it start sending? {0}".format(
                    self.vision_controller.tracking))
                self.toggle_send(sending=self.vision_controller.tracking,
                                 thread_name="BLUE_BLOCK",
                                 target=self.vision_controller.start_track_blue_cube,
                                 args=(self.client_address,)
                                 )
            case self.camera.msg_type:
                self.camera.sending = not self.camera.sending
                self.logger.log("Received CAMERA. Will it start sending? {0}".format(
                    self.camera.sending))
                self.toggle_send(sending=self.camera.sending,
                                 thread_name=self.camera.msg_type,
                                 target=self.camera.update_app_data,
                                 args=(self.client_address,)
                                 )
            case self.load_cell.msg_type:
                self.logger.log("Received LOAD_CELL")
                self.load_cell.sending = not self.load_cell.sending
                self.toggle_send(sending=self.load_cell.sending,
                                 thread_name=self.load_cell.msg_type,
                                 target=self.load_cell.update_app_data,
                                 args=(self.client_address,)
                                 )
            case "BLUE_BLOCK_VALUES":
                self.logger.log("Received BLUE_BLOCK_VALUES.")
                new_values = self.vision_controller.update_values(message)
                data = json.dumps(new_values)
                self.send_message(data.encode(), self.client_address)
            case self.accel_gyro_meter.msg_type:
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
        self.toggle_send_timeout_start = time.time()
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
        while time.time() < self.toggle_send_timeout_start + self.toggle_send_timeout:
            time.sleep(4)
            continue
        self.logger.log("App disconnected")
        self.__stop_components()
        self.app_components = self.__init_components()
        self.app_connected = False

    def stop_server(self):
        """
        Cleans up the server.
        """
        self.logger.log("Stopping the server...")
        self.timeout = 0
        self.toggle_send_timeout = 0
        self.app_connected = False
        self.__stop_components()

    def __stop_components(self):
        """
        Stops components from sending data.
        """
        for comp in self.app_components:
            comp.stop_sending()
            time.sleep(0.5)
        for thread in self.threads:
            if thread.name == "PING":
                continue
            thread.join()
            self.threads.remove(thread)
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
