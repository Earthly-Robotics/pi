import asyncio
import threading
import time

from ComponentControllers.ServoController import ServoController
from Components.WheelMotor import WheelMotor
from Utility import calculate_angle
from time import sleep
import math


class WheelsController:

    def __init__(self, servo_controller):
        self.network_controller = None
        self.servo_controller = servo_controller
        self.motor_left = WheelMotor(19, 26, 13)
        self.motor_right = WheelMotor(16, 20, 12)
        self.per_x = 0
        self.per_y = 0
        self.angle = 0
        self.last_angle = 0
        
    def move_wheels(self, x, y, limiter):
        """
        Moves the wheels based on joystick position
        :param limiter: Sets the max speed
        :param x: joystick x position
        :param y: joystick y position
        :return:
        """
        max_mid = 0  # Deadzone positive x and y
        min_mid = -400  # Deadzone negative x and y
        top = 2047
        bottom = 2047

        if min_mid < x < max_mid and min_mid < y < max_mid:
            self.stop()
        # forwards
        elif y > max_mid > x > min_mid:
            per_x = 0
            per_y = math.floor(((y - max_mid) / (top - max_mid)) * 100)
            self.angle = calculate_angle(0, y, 0, 2047)
            self.move(per_x, per_y, limiter)

        # backwards
        elif y < min_mid < x < max_mid:
            per_x = 0
            per_y = math.floor((y - min_mid) / (bottom + min_mid) * 100)
            self.angle = calculate_angle(0, y, 0, -2047)
            self.move(per_x, per_y, limiter)
        # left
        elif x < min_mid < y < max_mid:
            per_x = math.floor((x - min_mid) / (bottom + min_mid) * 100) * -1
            per_y = 0
            self.angle = calculate_angle(x, 0, 0, 2047) * -1
            self.move(per_x, per_y, limiter)
        # right
        elif x > max_mid > y > min_mid:
            per_x = math.floor((x - max_mid) / (top - max_mid) * 100) * -1
            per_y = 0
            self.angle = calculate_angle(x, 0, 0, 2047)
            self.move(per_x, per_y, limiter)
        # top-right
        elif x > max_mid and y > max_mid:
            per_x = math.floor((x - max_mid) / (top - max_mid) * 100) * -1
            per_y = math.floor((y - max_mid) / (top - max_mid) * 100)
            self.angle = calculate_angle(x, y, 0, 2047)
            self.move(per_x, per_y, limiter)
        # top-left
        elif x < min_mid and y > max_mid:
            per_x = math.floor((x - min_mid) / (bottom + min_mid) * 100) * -1
            per_y = math.floor((y - max_mid) / (top - max_mid) * 100)
            self.angle = calculate_angle(x, y, 0, 2047)
            self.move(per_x, per_y, limiter)
        # bottom-right
        elif x > max_mid and y < min_mid:
            per_x = math.floor((x - max_mid) / (top - max_mid) * 100) * -1
            per_y = math.floor((y - min_mid) / (bottom + min_mid) * 100)
            self.angle = 90 - calculate_angle(x, y, 0, -2047)
            self.move(per_x, per_y, limiter)
        # bottom-left
        elif x < min_mid and y < min_mid:
            per_x = math.floor((x - min_mid) / (bottom + min_mid) * 100) * -1
            per_y = math.floor((y - min_mid) / (bottom + min_mid) * 100)
            self.angle = 90 - calculate_angle(x, y, 0, -2047)
            self.move(per_x, per_y, limiter)

    def move(self, per_x, per_y, limiter):
        right_plus_left = ((100 - abs(per_x)) * (per_y / 100) + per_y)  # 200
        right_minus_left = ((100 - abs(per_y)) * (per_x / 100) + per_x)  # 0
        power_left_motor = (right_plus_left - right_minus_left) / 2
        power_right_motor = (right_plus_left + right_minus_left) / 2
        if self.angle >= self.last_angle():
            for i in range (self.last_angle, self.angle, 1):
                self.servo_controller.send_message("back wheel;" + str(i))
        else:
            for i in range(self.last_angle, self.angle, -1):
                self.servo_controller.send_message("back wheel;" + str(i))
        move_left_motor = asyncio.create_task(self.motor_left.move(math.floor(power_left_motor / limiter)))
        self.motor_right.move(math.floor(power_right_motor / limiter))
        await move_left_motor

    def turn_right(self):
        self.motor_left.move(math.floor(50))
        self.motor_right.move(math.floor(-50))

    def turn_left(self):
        self.motor_left.move(math.floor(-50))
        self.motor_right.move(math.floor(50))

    def stop(self):
        self.motor_left.move(0)
        self.motor_right.move(0)

# https://sensorkit.joy-it.net/en/sensors/ky-023
