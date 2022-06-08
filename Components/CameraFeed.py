import base64
import json
import pickle

import cv2 as cv
import numpy as np

from Network.NetworkController import NetworkController


class CameraFeed:
    camera = None
    active = False
    visionController = None

    def __init__(self, camera, visionController):
        self.camera = camera
        self.visionController = visionController

    def send_camera_feed(self, bool, network_controller):
        while bool:
            frame = self.camera.get_image()
            _, buffer = cv.imencode('.jpg', frame, [cv.IMWRITE_JPEG_QUALITY, 50])
            buffer = base64.b64encode(buffer).decode()
            msg = {"MT": "CameraFeed",
                   "FEED": buffer}
            msg = json.dumps(msg)
            network_controller.sendto(msg.encode(), (network_controller.ip_address, network_controller.port))
        self.camera.close()
