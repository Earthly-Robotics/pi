import platform
import socket
import json
import threading
import time

from Network.ConfigReader import config
from Logger.ConsoleLogger import ConsoleLogger
from Logger.FileLogger import FileLogger
from ComponentControllers.WheelsController import WheelsController
from threading import Thread


class NetworkController:

    threads = list()
    # def __init__(self, wheels_controller=WheelsController()):
    def __init__(self, wheels_controller):
        match platform.system():
            case "Windows":
                self.params = config()
                self.logger = ConsoleLogger()
            case "Linux":
                self.params = config('Pi')
                self.logger = FileLogger()
            case _:
                self.logger = FileLogger()
                self.logger.log("System not recognized")
        self.wheels_controller = wheels_controller
        self.ip_address = self.params['ip_address']
        self.port = int(self.params['port'])
        self.buffer_size = 1024
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.profile = 0
        self.line_dancing = False
        self.LD_thread_id = 0
        self.i = 0

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
            # print("Komt hier")
            bytes_address_pair = self.udp_server_socket.recvfrom(self.buffer_size)

            message = bytes_address_pair[0].decode()
            address = bytes_address_pair[1]
            self.client_address = address
            # print("Client address: ", address)

            try:
                message = json.loads(message)
                self.__handle_message(message)
            except json.JSONDecodeError as err:
                self.logger.log(str(err))
                bytes_to_send = str.encode("Message wasn't a JSON string")
                self.send_message(bytes_to_send, address)
        print("Loop Done listening")

    def __handle_message(self, message):
        match (message["MT"]):
            case "LJ":
                x = message["x"]
                y = message["y"]
                p = message["p"]
                if self.profile != p:
                    self.profile = p
                t = threading.Thread(target=self.wheels_controller.move_wheels, args=(x, y))
                self.wheels_controller.move_wheels(x, y)
                print("LeftJoystick: x : {}, y : {}, p : {}".format(x, y, p))
                msg_from_server = "Data LeftJoystick received"
                bytes_to_send = str.encode(msg_from_server)
                self.send_message(bytes_to_send, self.client_address)
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
                # msg_from_server = "Variable Button received"
                # bytes_to_send = str.encode(msg_from_server)
                # self.send_message(bytes_to_send, self.client_address)
            case "RJB":
                pass
            case "LJB":
                pass
            case "LD":
                self.logger.log("Start Line Dancing")
                # if self.line_dancing is False:
                #     self.line_dancing = not self.line_dancing
                #     message = {
                #         "MT": "LD",
                #         "B": "T"
                #     }
                #     json_string = json.dumps(message)
                #     bytes_to_send = str.encode(json_string)
                #     t = threading.Thread(target=self.continuously_send_message,
                #                          args=(bytes_to_send, self.client_address, 0), )
                #     t.name = "LD"
                #     self.threads.append(t)
                #     t.start()
                #     print(self.line_dancing)
                # else:
                #     print("Dispose Thread")
                #     self.line_dancing = not self.line_dancing
                #     for thread in self.threads:
                #         if thread.name == "LD":
                #             print("JAAAAAAAAAAAAAAA", self.line_dancing)
                #             thread.join()
                #             print("Thread Disposed")
                #             self.threads.remove(thread)
                #
                #     print("yesssssssssssssssssssssssssssssssssssssssssss", self.line_dancing)

            case "SD":
                self.logger.log("Start Solo Dancing")
            case "PS":
                self.logger.log("Start Planting Seeds")
            case "BR":
                self.logger.log("Start following block")
            case "CR":
                self.logger.log("Start driving through corner")
            case "CF":
                pass
            case _:
                self.logger.log("Not an existing MessageType")

    def continuously_send_message(self, bytes_to_send, address, interval):
        while self.line_dancing:
            self.send_message(bytes_to_send, address)
            time.sleep(interval)

    def send_message(self, bytes_to_send, address):
        self.udp_server_socket.sendto(bytes_to_send, address)
