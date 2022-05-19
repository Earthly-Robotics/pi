import os
import platform
import socket
import json
from configparser import ConfigParser


def config(section='PC'):
    """
    Returns an object containing the properties and values needed to connect to the corresponding database

    :param section: Is either "staging" or "final". Defines the section of the config file in database.ini.
    If not defined defaults to "staging"
    """
    while section not in ["PC", "Pi"]:
        print(f'\033[1;31mWrong dbType: {section}\nIt should be either "staging" or "final"\033[1;37m')
        return

    parser = ConfigParser()
    cwd = os.getcwd()
    if cwd[-1] == 'o':
        parser.read('../Config.ini')
    else:
        parser.read('Config.ini')

    values = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            values[param[0]] = param[1]
    else:
        raise Exception("Section {0} not found in database.ini".format(section))
    return values


class NetworkController:
    match platform.system():
        case "Windows":
            params = config()
        case "Linux":
            params = config('Pi')
        case _:
            print("System not recognized")

    def __init__(self):
        self.ip_address = NetworkController.params['ip_address']
        self.port = int(NetworkController.params['port'])
        self.buffer_size = 1024
        self.udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def setup_server(self):
        """
        Starts the server
        :return:
        """
        self.udp_server_socket.bind((self.ip_address, self.port))
        print("Server online")
        self.__start_listening()


    def __start_listening(self):
        """
        Starts listening for messages on the socket.
        :return:
        """
        print("Server started listening...")
        while True:
            bytes_address_pair = self.udp_server_socket.recvfrom(self.buffer_size)
            message = bytes_address_pair[0].decode()
            address = bytes_address_pair[1]

            try:
                message = json.loads(message)
                self.__handle_message(message)
            except json.JSONDecodeError as err:
                print(err)
                bytes_to_send = str.encode("Message wasn't a JSON string")
                self.send_message(bytes_to_send, address)

            msg_from_server = "Message received"

            bytes_to_send = str.encode(msg_from_server)

            # Sending a reply to client
            self.send_message(bytes_to_send, address)

    def __handle_message(self, message):
        match (message["MessageType"]):
            case "LeftJoystick":
                x = message["x"]
                y = message["y"]
                print("x : {}, y : {}".format(x, y))
            case "StartLineDancing":
                print("Start Line Dancing")
            case _:
                print("Not an existing MessageType")

    def send_message(self, bytes_to_send, address):
        self.udp_server_socket.sendto(bytes_to_send, address)













