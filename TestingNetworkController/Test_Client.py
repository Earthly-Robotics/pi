import socket
import json

msg = {
    "MessageType": "LeftJoystick",
    "x": "1.2",
    "y": "0.7"
}

msg_from_client = json.dumps(msg)

bytes_to_send = str.encode(msg_from_client)

server_address_port = ("127.0.0.1", 20001)

buffer_size = 1024

# Create a UDP socket at client side

udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket

udp_client_socket.sendto(bytes_to_send, server_address_port)

msg_from_server = udp_client_socket.recvfrom(buffer_size)
msg = "Message from Server: {}".format(msg_from_server[0].decode())

print(msg)
