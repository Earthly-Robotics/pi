import socket
import json

# Create JSON object to send to server.
import cv2
import cv2 as cv
import numpy, pickle

msg = {
    "MT": "CF"
}
msg_from_client = json.dumps(msg)
bytes_to_send = str.encode(msg_from_client)


server_address_port = ("127.0.0.1", 20001)
# server_address_port = ("142.252.29.102", 8080)
buffer_size = 1000000


# Create a UDP socket at client side
udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
udp_client_socket.sendto(bytes_to_send, server_address_port)
while True:
    # Receive Message from server.
    msg_from_server = udp_client_socket.recvfrom(buffer_size)
    clientip= msg_from_server[1][0]
    data = msg_from_server[0]
    data = pickle.loads(data)
    data = cv.imdecode(data,cv.IMREAD_COLOR)
    cv2.imshow('mypic', data)
    print("Received Message")
    if cv2.waitKey(10) == 13:  # Press Enter then window will close
        break
cv2.destroyAllWindows()
