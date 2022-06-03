import cv2 as cv
import numpy as np
from Components.Camera import Camera
from ComponentControllers.WheelsController import WheelsController


class VisionController:
    MAX_SPEED = 0.1
    DEBUG = False

    cam = None
    wheels_controller = None

    lower_area = 100
    upper_area = 800
    lower_shape = 5
    upper_shape = 14

    blue_low = np.uint8([[[0, 33, 86]]])
    blue_high = np.uint8([[[1, 149, 255]]])
    hsv_blue_low = cv.cvtColor(blue_low, cv.COLOR_RGB2HSV)
    hsv_blue_high = cv.cvtColor(blue_high, cv.COLOR_RGB2HSV)
    lower_blue_low = hsv_blue_low[0][0][0] - 10, 100, 100
    upper_blue_low = hsv_blue_low[0][0][0] + 10, 255, 255
    lower_blue_low = np.array(lower_blue_low)
    upper_blue_low = np.array(upper_blue_low)
    lower_blue_high = hsv_blue_high[0][0][0] - 10, 150, 150
    upper_blue_high = hsv_blue_high[0][0][0] + 10, 255, 255
    lower_blue_high = np.array(lower_blue_high)
    upper_blue_high = np.array(upper_blue_high)

    error = 0
    cam_half_width = 0

    def __init__(self):
        self.cam = Camera()
        self.wheels_controller = WheelsController()
        self.cam_half_width = self.cam.get_width() / 2

    def track_blue_cube(self):
        img = self.cam.get_image()
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        lower_mask = cv.inRange(hsv, self.lower_blue_low, self.upper_blue_low)
        upper_mask = cv.inRange(hsv, self.lower_blue_high, self.upper_blue_high)
        mask = lower_mask | upper_mask
        kernel = np.ones((9, 9), np.uint8)
        mask = cv2.erode(mask, kernel)
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv.contourArea(cnt)
            if self.lower_area < area < self.upper_area:
                approx = cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), False)
                if self.lower_shape < len(approx) < self.upper_shape:
                    if self.DEBUG:
                        cv.drawContours(img, [cnt], -1, (0, 255, 255), 2)
                    m = cv.moments(cnt)
                    center_x = int(m["m10"] / m["m00"])
                    self.error = self.cam_half_width - center_x
        if self.DEBUG:
            cv.imshow('result', img)
            cv.imshow('mask', mask)
        self.wheels_controller.set_velocity("left", - self.error * self.MAX_SPEED)
        self.wheels_controller.set_velocity("right", self.error * self.MAX_SPEED)

    def get_camera_feed(self):
        img = self.cam.get_image()
        cv.imshow('result', img)

