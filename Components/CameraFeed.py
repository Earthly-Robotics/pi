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

    def send_camera_feed(self, bool, netwerkcontroller):
        while bool:
            frame = self.camera.get_image()
            frame_encode = cv.imencode('.jpg', frame, [cv.IMWRITE_JPEG_QUALITY, 50])
            data_encode = np.array(frame_encode, dtype=object)
            byte_encode = data_encode.tobytes()
            netwerkcontroller.send_message(byte_encode, netwerkcontroller.client_address)
            cv.waitKey(1)
