import cv2 as cv
import numpy as np
from Camera import Camera
from WheelsController import WheelsController


class VisionController:
    MAX_SPEED = 0.1

    cam = None
    wheels_controller = None

    blue = np.uint8([[[255, 0, 0]]])
    hsv_blue = cv.cvtColor(blue, cv.COLOR_BGR2HSV)
    lower_limit = np.array([100, 150, 0], np.uint8)
    upper_limit = np.array([140, 255, 255], np.uint8)

    error = 0
    cam_half_width = 0

    def __init__(self, robot, time_step):
        self.cam = Camera(robot, time_step)
        self.wheels_controller = WheelsController(robot)
        self.cam_half_width = self.cam.get_width() / 2

    def get_image_from_camera(self):
        image = self.cam.get_image_array_from_camera()
        image = np.asarray(image, dtype=np.uint8)
        image = cv.cvtColor(image, cv.COLOR_BGRA2RGB)
        image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
        return cv.flip(image, 1)

    def track_blue_cube(self):
        img = self.get_image_from_camera()
        img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = cv.inRange(img, self.lower_limit, self.upper_limit)
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            largest_contour = max(contours, key=cv.contourArea)
            largest_contour_center = cv.moments(largest_contour)

            if largest_contour_center['m00'] > 0:
                center_x = int(largest_contour_center['m10'] / largest_contour_center['m00'])
                self.error = self.cam_half_width - center_x
        self.wheels_controller.set_velocity("left", - self.error * self.MAX_SPEED)
        self.wheels_controller.set_velocity("right", self.error * self.MAX_SPEED)

