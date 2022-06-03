import cv2 as cv


class Camera:
    camera = None

    def __init__(self):
        self.camera = cv.VideoCapture(0)

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
