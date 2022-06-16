import asyncio
import base64
import json
import threading
import time
import platform

import cv2 as cv
import numpy as np
from Components.Camera import Camera
from ComponentControllers.WheelsController import WheelsController


class VisionController:
    MAX_SPEED = 0.1
    DEBUG = True
    tracking = False

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

    def __init__(self, cam, wheels_controller, network_controller):
        self.client_ip = None
        self.cam = cam
        self.wheels_controller = wheels_controller
        self.network_controller = network_controller
        self.cam_half_width = self.cam.get_width() / 2

    def start_track_blue_cube(self, client_ip):
        asyncio.run(self.track_blue_cube(client_ip))

    async def track_blue_cube(self, client_ip):
        self.client_ip = client_ip
        while self.tracking:
            start = time.time()
            img = self.cam.get_image()
            if img is None:
                pass
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            lower_mask = cv.inRange(hsv, self.lower_blue_low, self.upper_blue_low)
            upper_mask = cv.inRange(hsv, self.lower_blue_high, self.upper_blue_high)
            mask = lower_mask | upper_mask
            kernel = np.ones((9, 9), np.uint8)
            mask = cv.erode(mask, kernel)
            contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            self.error = 0
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
            os = platform.system()
            if self.DEBUG and os == "Windows":
                cv.imshow('result', img)
                cv.imshow('mask', mask)
            elif self.DEBUG and os == "Linux":
                send_feed_task = asyncio.create_task(self.send_feed(img))
                if self.error > 0:
                    self.wheels_controller.turn_right()
                elif self.error < 0:
                    self.wheels_controller.turn_left()
                else:
                    self.wheels_controller.stop()
            # self.wheels_controller.set_velocity("left", - self.error * self.MAX_SPEED)  # Linker Wiel
            # self.wheels_controller.set_velocity("right", self.error * self.MAX_SPEED)  # Rechter Wiel
            if self.DEBUG and os == "Linux":
                await asyncio.gather(send_feed_task)
                time.sleep(max(1. / 24 - (time.time() - start), 0))

    async def send_feed(self, img):
        _, data = cv.imencode('.jpg', img, [cv.IMWRITE_JPEG_QUALITY, 50])
        data = base64.b64encode(data).decode()
        msg_obj = {
            "MT": "CAMERA_DEBUG",
            "Camera_Debug": data
        }
        json_string = json.dumps(msg_obj)
        msg = str.encode(json_string)
        self.network_controller.send_message(msg, self.client_ip)

    def update_values(self, msg):
        parsed = self.__int_try_parse(msg["Lower_Area"])
        if parsed[1]:
            self.lower_area = parsed[0]
            print("lower_area: ", self.lower_area)
        parsed = self.__int_try_parse(msg["Upper_Area"])
        if parsed[1]:
            self.upper_area = parsed[0]
            print("upper_area: ", self.lower_area)
        parsed = self.__int_try_parse(msg["Lower_Shape"])
        if parsed[1]:
            self.lower_shape = parsed[0]
            print("lower_shape: ", self.lower_area)
        parsed = self.__int_try_parse(msg["Upper_Shape"])
        if parsed[1]:
            self.upper_shape = parsed[0]
            print("upper_shape: ", self.lower_area)
        return self.get_values()

    def get_values(self):
        return {
            "MT": "BLUE_BLOCK_VALUES",
            "Lower_Area": self.lower_area,
            "Upper_Area": self.upper_area,
            "Lower_Shape": self.lower_shape,
            "Upper_Shape": self.upper_shape
        }

    def __int_try_parse(self, value):
        try:
            return int(value), True
        except ValueError:
            return value, False

    def stop_sending(self):
        self.tracking = False
