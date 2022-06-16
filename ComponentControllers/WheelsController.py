import threading
import time

from Components.WheelMotor import WheelMotor
from time import sleep
import math


class WheelsController:

    def __init__(self):
        self.network_controller = None
        self.motor_left = WheelMotor(19, 26, 13)
        self.motor_right = WheelMotor(16, 20, 12)
        self.per_x = 0
        self.per_y = 0
        
    def move_wheels(self, x, y):
        """
        Moves the wheels based on joystick position
        :param x: joystick x position
        :param y: joystick y position
        :return:
        """
        max_mid = 0  # Deadzone positive x and y
        min_mid = -400  # Deadzone negative x and y
        Top = 2047
        Bottom = 2047

        # if min_mid < x < max_mid and min_mid < y < max_mid:
        #     power_left_motor = 0
        #     power_right_motor = 0
        #     self.motor_left.move(power_left_motor)
        #     self.motor_right.move(power_right_motor)
        # else:
        #     x = math.floor((x / 1750) * 100) * -1
        #     y = math.floor((y / 1750) * 100)
        #
        #     right_plus_left = (100-abs(x)) * (y/100) + y
        #     right_minus_left = (100-abs(y)) * (x/100) + x
        #     power_left_motor = (right_plus_left-right_minus_left)/2
        #     power_right_motor = (right_plus_left+right_minus_left)/2
        #     print("Left power: ", power_left_motor)
        #     # print("Right power: ", power_right_motor)
        #     if power_left_motor > 100:
        #         power_left_motor = 100
        #     if power_left_motor < -100:
        #         power_left_motor = -100
        #     if power_right_motor > 100:
        #         power_right_motor = 100
        #     if power_right_motor < -100:
        #         power_right_motor = -100
        #     self.motor_left.move(math.floor(power_left_motor))
        #     self.motor_right.move(math.floor(power_right_motor))

        # power_left = 0
        # power_right = 0

        if min_mid < x < max_mid and min_mid < y < max_mid:
            self.stop()
        # forwards
        elif y > max_mid > x > min_mid:
            per_x = 0
            per_y = math.floor(((y - max_mid) / (Top - max_mid)) * 100)
            self.move(per_x, per_y)

        # backwards
        elif y < min_mid < x < max_mid:
            per_x = 0
            per_y = math.floor((y - min_mid) / (Bottom + min_mid) * 100)
            self.move(per_x, per_y)
        # left
        elif x < min_mid < y < max_mid:
            per_x = math.floor((x - min_mid) / (Bottom + min_mid) * 100) * -1
            per_y = 0
            self.move(per_x, per_y)
        # right
        elif x > max_mid > y > min_mid:
            per_x = math.floor((x - max_mid) / (Top - max_mid) * 100) * -1
            per_y = 0
            self.move(per_x, per_y)
        # top-right
        elif x > max_mid and y > max_mid:
            per_x = math.floor((x - max_mid) / (Top - max_mid) * 100) * -1
            per_y = math.floor((y - max_mid) / (Top - max_mid) * 100)
            self.move(per_x, per_y)
        # top-left
        elif x < min_mid and y > max_mid:
            per_x = math.floor((x - min_mid) / (Bottom + min_mid) * 100) * -1
            per_y = math.floor((y - max_mid) / (Top - max_mid) * 100)
            self.move(per_x, per_y)
        # bottom-right
        elif x > max_mid and y < min_mid:
            per_x = math.floor((x - max_mid) / (Top - max_mid) * 100) * -1
            per_y = math.floor((y - min_mid) / (Bottom + min_mid) * 100)
            self.move(per_x, per_y)
        # bottom-left
        elif x < min_mid and y < min_mid:
            per_x = math.floor((x - min_mid) / (Bottom + min_mid) * 100) * -1
            per_y = math.floor((y - min_mid) / (Bottom + min_mid) * 100)
            self.move(per_x, per_y)

    def move(self, per_x, per_y):
        right_plus_left = ((100 - abs(per_x)) * (per_y / 100) + per_y)  # 200
        right_minus_left = ((100 - abs(per_y)) * (per_x / 100) + per_x)  # 0
        power_left_motor = (right_plus_left - right_minus_left) / 2
        power_right_motor = (right_plus_left + right_minus_left) / 2
        self.motor_left.move(math.floor(power_left_motor))
        self.motor_right.move(math.floor(power_right_motor))

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
