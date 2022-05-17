import socket
import json


def main():
    setup_server()
    # Listen for incoming datagrams

    while True:
        print("Server started listening...")
        receive_message(udp_server_socket, buffer_size)


def setup_server():
    local_ip = "127.0.0.1"
    local_port = 20001
    buffer_size = 1024
    # Create a datagram socket
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Bind to address and ip
    udp_server_socket.bind((local_ip, local_port))
    print("UDP server online")
    return buffer_size

def receive_message(udp_server_socket, buffer_size):
    bytes_address_pair = udp_server_socket.recvfrom(buffer_size)
    message = bytes_address_pair[0].decode()
    address = bytes_address_pair[1]

    message = json.loads(message)
    handle_message(message)
    client_msg = "Message from Client: {}".format(message["MessageType"])
    client_ip = "Client IP Address:{}".format(address)

    print(client_msg)
    print(client_ip)

    msg_from_server = "Hello UDP Client"

    bytes_to_send = str.encode(msg_from_server)

    # Sending a reply to client
    send_message(udp_server_socket, bytes_to_send, address)
    return message

def send_message(udp_server_socket, bytes_to_send, address):
    print("Sending message...")
    udp_server_socket.sendto(bytes_to_send, address)
    print("Message send")


def handle_message(message):
    match(message["MessageType"]):
        case "LeftJoystick":
            x = message["x"]
            y = message["y"]
            print("x : {}, y : {}".format(x, y))
        case _:
            print("Not an existing MessageType")


main()
