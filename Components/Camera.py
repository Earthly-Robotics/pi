import base64
import cv2 as cv

from Components.AppComponent import AppComponent


class Camera(AppComponent):

    def __init__(self, network_controller):
        super().__init__(network_controller)
        self.camera = cv.VideoCapture(0)
        self.msg_type = "CAMERA"

    def get_image(self):
        if self.camera is not None:
            ret, frame = self.camera.read()
            return frame
        else:
            print("Camera does not exist. Try calling setup()")
            return None

    def get_width(self):
        if self.camera is not None:
            return self.camera.get(3)
        else:
            print("Camera does not exist. Try calling setup()")
            return None

    def format_component_data(self) -> tuple:
        frame = self.get_image()
        _, buffer = cv.imencode('.jpg', frame, [cv.IMWRITE_JPEG_QUALITY, 50])
        buffer = base64.b64encode(buffer).decode()
        return "Camera", buffer
