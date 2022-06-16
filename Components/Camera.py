import base64
import time
import cv2 as cv
from Components.AppComponent import AppComponent


class Camera(AppComponent):
    def __init__(self, network_controller):
        super().__init__(network_controller)
        self.msg_type = "CAMERA"
        self.camera = cv.VideoCapture(0)
        if not self.camera.isOpened():
            raise Exception("Couldn't open camera")

    def get_image(self):
        if self.camera is not None and self.camera.isOpened():
            ret, frame = self.camera.read()
            return frame
        else:
            return None

    def get_width(self):
        if self.camera is not None:
            return self.camera.get(3)
        else:
            return None

    def format_component_data(self) -> tuple:
        start = time.time()
        frame = self.get_image()
        _, buffer = cv.imencode('.jpg', frame, [cv.IMWRITE_JPEG_QUALITY, 50])
        buffer = base64.b64encode(buffer).decode()
        self.interval = max(1. / 24 - (time.time() - start), 0)
        return "Camera", buffer
