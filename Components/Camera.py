import base64
import time
import cv2 as cv
from threading import Thread
from Components.AppComponent import AppComponent


class Camera(AppComponent):
    def __init__(self, network_controller):
        super().__init__(network_controller)
        self._process = None
        self.msg_type = "CAMERA"
        self.capturing = False
        self.frame_rate = 24
        self.camera = cv.VideoCapture(0)
        _, self._current_frame = self.camera.read()
        self.interval = 0
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

    def get_height(self):
        if self.camera is not None:
            return self.camera.get(4)
        else:
            return None

    def _capture_frame(self):
        prev = 0
        while self.capturing:
            time_elapsed = time.time() - prev
            frame = self.get_image()

            if frame is not None and time_elapsed > 1. / self.frame_rate:
                prev = time.time()
                self._current_frame = frame

    def start_capturing(self):
        if self.capturing is True:
            return
        self.capturing = True
        self._process = Thread(target=self._capture_frame, args=())
        self._process.start()
        return self

    def get_frame(self):
        return self._current_frame

    def stop_capturing(self):
        if self.capturing is False:
            return
        self.capturing = False
        self._process.join()
        return self

    def format_component_data(self) -> tuple:
        frame = self.get_frame()
        if frame is None:
            return None
        _, buffer = cv.imencode('.jpg', frame, [cv.IMWRITE_JPEG_QUALITY, 50])
        buffer = base64.b64encode(buffer).decode()
        return "Camera", buffer
