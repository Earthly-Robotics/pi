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
        :param x: The x value of the joystick
        :param y: The y value of the joystick
        :param limiter: limits the speed
        """
        deadzone_max = 0  # Maximal deadzone value
        deadzone_min = -400  # Minimal deadzone value
        max_value = 2047
        min_value = -2047

        # Checks if joystick is in the middle.
        if deadzone_min < x < deadzone_max and deadzone_min < y < deadzone_max:
            self.stop()

        # Top of middle
        elif y > deadzone_max > x > deadzone_min:
            # X is in the middle. So the percentage is 0.
            per_x = 0
            # calculates the percentage of y based on how far it is from the max_value. If y is equal to max-value, per_y is 100%.
            per_y = math.floor(((y - deadzone_max) / (max_value - deadzone_max)) * 100)
            self.angle = math.floor(calculate_angle(0, y, 0, 2047))
            self.move(per_x, per_y, limiter)

        # Bottom of middle
        elif y < deadzone_min < x < deadzone_max:
            # X is in the middle. So the percentage is 0.
            per_x = 0
            # calculates the percentage of y based on how far it is from the min_value. If y is equal to min-value, per_y is 100%.
            per_y = math.floor((y - deadzone_min) / (-1 * min_value + deadzone_min) * 100)
            self.angle = math.floor(calculate_angle(0, y, 0, -2047))
            self.move(per_x, per_y, limiter)
        # Left of middle
        elif x < deadzone_min < y < deadzone_max:
            # calculates the percentage of x based on how far it is from the min_value. If x is equal to min-value, per_x is 100%.
            per_x = math.floor((x - deadzone_min) / (-1 * min_value + deadzone_min) * 100) * -1
            # Y is in the middle. So percentage is 0.
            per_y = 0
            self.angle = math.floor(calculate_angle(x, 0, 0, 2047) * -1)
            self.move(per_x, per_y, limiter)
        # Right of middle
        elif x > deadzone_max > y > deadzone_min:
            # calculates the percentage of x based on how far it is from the max_value. If x is equal to max-value, per_x is 100%.
            per_x = math.floor((x - deadzone_max) / (max_value - deadzone_max) * 100) * -1
            # Y is in the middle. So percentage is 0.
            per_y = 0
            self.angle = math.floor(calculate_angle(x, 0, 0, 2047))
            self.move(per_x, per_y, limiter)
        # Top right of middle
        elif x > deadzone_max and y > deadzone_max:
            # calculates the percentage of x based on how far it is from the max_value. If x is equal to max-value, per_x is 100%.
            per_x = math.floor((x - deadzone_max) / (max_value - deadzone_max) * 100) * -1
            # calculates the percentage of y based on how far it is from the max_value. If y is equal to max-value, per_y is 100%.
            per_y = math.floor((y - deadzone_max) / (max_value - deadzone_max) * 100)
            self.angle = math.floor(calculate_angle(x, y, 0, 2047))
            self.move(per_x, per_y, limiter)
        # Top left of middle
        elif x < deadzone_min and y > deadzone_max:
            # calculates the percentage of x based on how far it is from the min_value. If x is equal to min-value, per_x is 100%.
            per_x = math.floor((x - deadzone_min) / (-1 * min_value + deadzone_min) * 100) * -1
            # calculates the percentage of y based on how far it is from the max_value. If y is equal to max-value, per_y is 100%.
            per_y = math.floor((y - deadzone_max) / (max_value - deadzone_max) * 100)
            self.angle = math.floor(calculate_angle(x, y, 0, 2047))
            self.move(per_x, per_y, limiter)
        # Bottom right of middle
        elif x > deadzone_max and y < deadzone_min:
            # calculates the percentage of x based on how far it is from the max_value. If x is equal to max-value, per_x is 100%.
            per_x = math.floor((x - deadzone_max) / (max_value - deadzone_max) * 100) * -1
            # calculates the percentage of y based on how far it is from the min_value. If y is equal to min-value, per_y is 100%.
            per_y = math.floor((y - deadzone_min) / (-1 * min_value + deadzone_min) * 100)
            self.angle = 90 - math.floor(calculate_angle(x, y, 0, -2047))
            self.move(per_x, per_y, limiter)
        # Bottom left of middle
        elif x < deadzone_min and y < deadzone_min:
            # calculates the percentage of x based on how far it is from the min_value. If x is equal to min-value, per_x is 100%.
            per_x = math.floor((x - deadzone_min) / (-1 * min_value + deadzone_min) * 100) * -1
            # calculates the percentage of y based on how far it is from the min_value. If y is equal to min-value, per_y is 100%.
            per_y = math.floor((y - deadzone_min) / (-1 * min_value + deadzone_min) * 100)
            self.angle = math.floor(90 - calculate_angle(x, y, 0, -2047))
            self.move(per_x, per_y, limiter)

    def move(self, per_x, per_y, limiter):
        right_plus_left = ((100 - abs(per_x)) * (per_y / 100) + per_y)  # 200
        right_minus_left = ((100 - abs(per_y)) * (per_x / 100) + per_x)  # 0
        power_left_motor = (right_plus_left - right_minus_left) / 2
        power_right_motor = (right_plus_left + right_minus_left) / 2
        print(self.angle)
        # if self.angle >= self.last_angle:
        #     for i in range(self.last_angle, self.angle, 1):
        #         self.servo_controller.send_message("back wheel;" + str(self.angle))
        # else:
        #     for i in range(self.last_angle, self.angle, -1):
        #         self.servo_controller.send_message("back wheel;" + str(self.angle))
        # self.motor_left.move(math.floor(power_left_motor / limiter))
        # self.motor_right.move(math.floor(power_right_motor / limiter))

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
