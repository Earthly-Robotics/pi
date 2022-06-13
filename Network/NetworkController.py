import platform
import socket
import json
import threading
import time

from Components.LoadCell import LoadCell
from Components.GyroAccelerometer import GyroAccelerometer
from Network.ConfigReader import config
from Logger.ConsoleLogger import ConsoleLogger
from Logger.FileLogger import FileLogger


# from ComponentControllers.WheelsController import WheelsController


class NetworkController:
    threads = list()
    load_cell = None

    # def __init__(self, wheels_controller=WheelsController()):
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
        # self.wheels_controller = wheels_controller
        self.ip_address = self.params['ip_address']
        self.port = int(self.params['port'])
        self.buffer_size = 1024
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.profile = 0
        self.line_dancing = False
        self.LD_thread_id = 0

        self.load_cell = LoadCell(network_controller=self)
        self.accel_gyro_meter = GyroAccelerometer(network_controller=self)

    def setup_server(self):
        """
        Starts the server
        :return:
        """
        self.udp_server_socket.bind((self.ip_address, self.port))
        self.logger.log("Server online")
        self.__start_listening()

    def __start_listening(self):
        """
        Starts listening for messages on the socket.
        :return:
        """
        print("Own IP: ", self.ip_address)
        print("Own Port: ", self.port)
        self.logger.log("Server started listening...")
        while True:
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

    def __handle_message(self, message):
        match (message["MT"]):
            case "LJ":
                pass
                # x = message["x"]
                # y = message["y"]
                # p = message["p"]
                # if self.profile != p:
                #     self.profile = p
                # # self.wheels_controller.move_wheels(x, y)
                # # print("LeftJoystick: x : {}, y : {}".format(x, y))
                # msg_from_server = "Data LeftJoystick received"
                # bytes_to_send = str.encode(msg_from_server)
                # self.send_message(bytes_to_send, self.client_address)
            case "RJ":
                pass
                # x = message["x"]
                # y = message["Y"]
                # p = message["p"]
                # if self.profile != p:
                #     self.profile = p
                # self.logger.log("RightJoystick: x : {}, y : {}".format(x, y))
                # msg_from_server = "Data RightJoystick received"
                # bytes_to_send = str.encode(msg_from_server)
                # self.send_message(bytes_to_send, self.client_address)
            case "PB":
                p = message["p"]
                self.profile = p
                msg_from_server = "Profile Button received"
                bytes_to_send = str.encode(msg_from_server)
                self.send_message(bytes_to_send, self.client_address)
            case "VB":
                msg_from_server = "Variable Button received"
                bytes_to_send = str.encode(msg_from_server)
                self.send_message(bytes_to_send, self.client_address)
            case "RJB":
                pass
            case "LJB":
                pass
            case "LD":
                pass
            case "SOLO_DANCE":
                self.logger.log("Start Solo Dancing")
            case "PLANT":
                self.logger.log("Start Planting Seeds")
            case "BLUE_BLOCK":
                self.logger.log("Start following block")
            case "CAMERA":
                pass
            case "CAMERA_DEBUG":
                pass
            case self.load_cell.msg_type:
                self.load_cell.sending = not self.load_cell.sending
                self.toggle_send(sending=self.load_cell.sending,
                                 thread_name=self.load_cell.msg_type,
                                 target=self.load_cell.update_app_data,
                                 args=(self.client_address,))
            case self.accel_gyro_meter.msg_type:
                self.accel_gyro_meter.sending = not self.accel_gyro_meter.sending
                self.toggle_send(sending=self.accel_gyro_meter.sending,
                                 thread_name=self.accel_gyro_meter.msg_type,
                                 target=self.accel_gyro_meter.update_app_data,
                                 args=(self.client_address,))
            case _:
                self.logger.log("Not an existing MessageType")

    def toggle_send(self, sending, thread_name, target, args):
        if sending is False:
            for thread in self.threads:
                if thread.name == thread_name:
                    thread.join()
                    self.threads.remove(thread)
        else:
            t = threading.Thread(target=target,
                                 args=args)
            t.name = thread_name
            self.threads.append(t)
            t.start()

    def send_message(self, bytes_to_send, address):
        self.udp_server_socket.sendto(bytes_to_send, address)
