import asyncio
import base64
import platform
import socket
import json
import threading
import time

from ComponentControllers.ServoController import ServoController
from CameraFeed import CameraFeed
from ComponentControllers.SoundController import SoundController
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
        self.limiter = 1
        self.rotate_magnet = False
        self.timeout = 600
        self.timeout_start = 0
        self.toggle_send_timeout = 600
        self.toggle_send_timeout_start = 0
        self.app_connected = False

        self.sound_controller = SoundController()
        self.wheels_controller = WheelsController()
        self.servo_controller = ServoController()
        self.app_components = self.__init_components()

    def __init_components(self):
        app_components = []

        self.load_cell = LoadCell(network_controller=self)
        app_components.append(self.load_cell)

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
        self.sound_controller.get_beat()

        #TODO: uncomment this

        # match (message["MT"]):
        #     case "LJ":
        #         x = message["x"]
        #         y = message["y"]
        #         p = message["p"]
        #         if self.profile != p:
        #             self.profile = p
        #         LJ_thread = threading.Thread(target=self.wheels_controller.move_wheels, args=(x, y))
        #         LJ_thread.start()
        #         # self.wheels_controller.move_wheels(x, y)
        #         # print("LeftJoystick: x : {}, y : {}, p : {}".format(x, y, p))
        #     case "RJ":
        #         pass
        #         # x = message["x"]
        #         # y = message["y"]
        #         # p = message["p"]
        #         # if self.profile != p:
        #         #     self.profile = p
        #         # self.logger.log("RightJoystick: x : {}, y : {}".format(x, y))
        #         # msg_from_server = "Data RightJoystick received"
        #         # bytes_to_send = str.encode(msg_from_server)
        #         # self.send_message(bytes_to_send, self.client_address)
        #     case "PB":
        #         pass
        #         # p = message["p"]
        #         # self.profile = p
        #         # msg_from_server = "Profile Button received"
        #         # bytes_to_send = str.encode(msg_from_server)
        #         # self.send_message(bytes_to_send, self.client_address)
        #     case "VB":
        #         pass
        #     case "RJB":
        #         pass
        #     case "LJB":
        #         pass
        #     case "PING":
        #         self.toggle_send_timeout_start = time.time()
        #         self.logger.log("Received PING.")
        #         if not self.app_connected:
        #             for thread in self.threads:
        #                 if thread.name == "PING":
        #                     thread.join()
        #             self.app_connected = True
        #             self.logger.log("App connected")
        #             t = threading.Thread(target=self.check_toggle_send_connection)
        #             t.name = "PING"
        #             self.threads.append(t)
        #             t.start()
        #         ping = {
        #             "MT": "PING"
        #         }
        #         data = json.dumps(ping)
        #         self.send_message(data.encode(), self.client_address)
        #     case "LINE_DANCE":
        #         pass
        #     case "SOLO_DANCE":
        #         pass
        #     case "PLANT":
        #         pass
        #     case "BLUE_BLOCK":
        #         if self.vision_controller is None:
        #             self.logger.log("Can't process BLUE_BLOCK. Vision_Controller is None")
        #             return
        #         self.vision_controller.tracking = not self.vision_controller.tracking
        #         self.logger.log("Received BLUE_BLOCK. Will it start sending? {0}".format(
        #             self.vision_controller.tracking))
        #         self.toggle_send(sending=self.vision_controller.tracking,
        #                          thread_name="BLUE_BLOCK",
        #                          target=self.vision_controller.start_track_blue_cube,
        #                          args=(self.client_address,)
        #                          )
        #         block_values = self.vision_controller.get_values()
        #         data = json.dumps(block_values)
        #         self.send_message(data.encode(), self.client_address)
        #     case "CAMERA":
        #         if self.camera is None:
        #             self.logger.log("Can't process CAMERA. Camera is None")
        #             return
        #         self.camera.sending = not self.camera.sending
        #         self.logger.log("Received CAMERA. Will it start sending? {0}".format(
        #             self.camera.sending))
        #         self.toggle_send(sending=self.camera.sending,
        #                          thread_name=self.camera.msg_type,
        #                          target=self.camera.update_app_data,
        #                          args=(self.client_address,)
        #                          )
        #     case "CAMERA_DEBUG":
        #         pass
        #         # if self.camera_feed is None:
        #         #     self.logger.log("Can't process CAMERA_DEBUG. Camera_Feed is None")
        #         # self.logger.log("Received CAMERA_DEBUG")
        #         # self.camera_feed.sending = not self.camera_feed.sending
        #         # self.toggle_send(sending=self.camera_feed.sending,
        #         #                  thread_name=self.camera_feed.msg_type,
        #         #                  target=self.camera_feed.update_app_data,
        #         #                  args=(self.client_address,))
        #
        #     case "WEIGHT":
        #         if self.load_cell is None:
        #             self.logger.log("Can't process WEIGHT. Load_cell is None")
        #             return
        #         self.logger.log("Received WEIGHT")
        #         self.load_cell.sending = not self.load_cell.sending
        #         self.toggle_send(sending=self.load_cell.sending,
        #                          thread_name=self.load_cell.msg_type,
        #                          target=self.load_cell.update_app_data,
        #                          args=(self.client_address,)
        #                          )
        #     case "BLUE_BLOCK_VALUES":
        #         if self.vision_controller is None:
        #             self.logger.log("Can't process BLUE_BLOCK_VALUES. Vision Controller is None")
        #             return
        #         self.logger.log("Received BLUE_BLOCK_VALUES.")
        #         new_values = self.vision_controller.update_values(message)
        #         data = json.dumps(new_values)
        #         self.send_message(data.encode(), self.client_address)
        #     case "VELOCITY":
        #         if self.accel_gyro_meter is None:
        #             self.logger.log("Can't process VELOCITY. Accel_Gyro_Meter is None")
        #             return
        #         self.logger.log("Received VELOCITY.")
        #         self.accel_gyro_meter.sending = not self.accel_gyro_meter.sending
        #         self.toggle_send(sending=self.accel_gyro_meter.sending,
        #                          thread_name=self.accel_gyro_meter.msg_type,
        #                          target=self.accel_gyro_meter.update_app_data,
        #                          args=(self.client_address,)
        #                          )
        #     case "EMERGENCY_BUTTON":
        #         self.logger.log("EMERGENCY_BUTTON received. Stopping all components")
        #         self.__stop_components()
        #         self.app_components = self.__init_components()
        #         data = json.dumps({
        #             "MT": "MANUAL"
        #         })
        #         self.send_message(data.encode(), self.client_address)
        #     case _:
        #         self.logger.log("{0} is not an existing MessageType".format(message["MT"]))

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
