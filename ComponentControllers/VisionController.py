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
    DEBUG = True
    tracking = False

    cam = None
    wheels_controller = None

    lower_area = 200
    upper_area = 700
    lower_shape = 7
    upper_shape = 24

    lower_blue = np.array([60, 29, 11])
    upper_blue = np.array([119, 236, 202])

    error = 0
    cam_half_width = 0

    def __init__(self, cam, wheels_controller, network_controller):
        self.client_ip = None
        self.cam = cam
        self.wheels_controller = wheels_controller
        self.network_controller = network_controller
        if self.cam is not None:
            self.cam_half_width = self.cam.get_width() // 2
            half_height = self.cam.get_height() // 2
            self.w = 300
            self.h = 200
            self.x = int(self.cam_half_width - self.w / 2)
            self.y = int(half_height - self.h / 2)

    def start_track_blue_cube(self, client_ip):
        asyncio.run(self.track_blue_cube(client_ip))

    async def track_blue_cube(self, client_ip):
        self.client_ip = client_ip
        while self.tracking:
            if self.cam is None:
                continue
            img = self.cam.get_frame()
            if img is None:
                continue
            img = img[self.y:self.y + self.h, self.x:self.x + self.w]
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
            mask = cv.inRange(hsv, self.lower_blue, self.upper_blue)
            kernel = np.ones((7, 7), np.uint8)
            mask = cv.erode(mask, kernel)
            contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            self.error = 0
            for cnt in contours:
                area = cv.contourArea(cnt)
                if self.lower_area < area < self.upper_area:
                    approx = cv.approxPolyDP(cnt, 0.01 * cv.arcLength(cnt, True), False)
                    if self.lower_shape < len(approx) < self.upper_shape:
                        if self.DEBUG:
                            cv.drawContours(img, [cnt], -1, (0, 255, 255), 2)  # Draws a yellow outline
                        m = cv.moments(cnt)
                        center_x = int(m["m10"] / m["m00"])
                        self.error = 100 / (self.w // 2) * ((self.w // 2) - center_x)
            os = platform.system()
            if self.DEBUG and os == "Windows":
                cv.imshow('result', img)
                cv.imshow('mask', mask)
            elif self.DEBUG and os == "Linux":
                task = asyncio.create_task(self.send_feed(img))
                if abs(self.error) < 30:
                    self.error = 0
                    self.wheels_controller.stop()
                elif self.error < 0:
                    self.error = abs(max(self.error, -50))
                    self.wheels_controller.turn_right(self.error)
                elif self.error > 0:
                    self.error = abs(min(self.error, 50))
                    self.wheels_controller.turn_left(self.error)
                await task

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
        parsed = self.__int_try_parse(msg["Upper_Area"])
        if parsed[1]:
            self.upper_area = parsed[0]
        parsed = self.__int_try_parse(msg["Lower_Shape"])
        if parsed[1]:
            self.lower_shape = parsed[0]
        parsed = self.__int_try_parse(msg["Upper_Shape"])
        if parsed[1]:
            self.upper_shape = parsed[0]
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
