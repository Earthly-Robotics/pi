import platform
from Network.ConfigReader import config
import socket
import json
from Logger.ConsoleLogger import ConsoleLogger
from Logger.FileLogger import FileLogger


class NetworkController:

    def __init__(self):
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
        self.ip_address = self.params['ip_address']
        self.port = int(self.params['port'])
        self.buffer_size = 1024
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.profile = 0

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
        print(self.ip_address)
        print(self.port)
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
                x = message["x"]
                y = message["y"]
                p = message["p"]
                if self.profile != p:
                    self.profile = p
                self.logger.log("LeftJoystick: x : {}, y : {}".format(x, y))
                msg_from_server = "Data LeftJoystick received"
                bytes_to_send = str.encode(msg_from_server)
                self.send_message(bytes_to_send, self.client_address)
            case "RJ":
                x = message["x"]
                y = message["Y"]
                p = message["p"]
                if self.profile != p:
                    self.profile = p
                self.logger.log("RightJoystick: x : {}, y : {}".format(x, y))
                msg_from_server = "Data RightJoystick received"
                bytes_to_send = str.encode(msg_from_server)
                self.send_message(bytes_to_send, self.client_address)
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
                print()
            case "LJB":
                print()
            case "StartLineDancing":
                self.logger.log("Start Line Dancing")
            case _:
                self.logger.log("Not an existing MessageType")

    def send_message(self, bytes_to_send, address):
        self.udp_server_socket.sendto(bytes_to_send, address)
