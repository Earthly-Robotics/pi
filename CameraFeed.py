import cv2 as cv
import base64
import time
import json

from Components.AppComponent import AppComponent


class CameraFeed(AppComponent):

    def __init__(self, network_controller, vision_controller):
        super().__init__(network_controller)
        self.msg_type = "CAMERA_DEBUG"
        self.vision_controller = vision_controller

    def format_component_data(self) -> tuple:
        start = time.time()
        img = self.vision_controller.get_debug_image()
        if img is None:
            return None
        _, data = cv.imencode('.jpg', img, [cv.IMWRITE_JPEG_QUALITY, 50])
        data = base64.b64encode(data).decode()
        time.sleep(max(1. / 24 - (time.time() - start), 0))
        return "Camera_Debug", str(data)

