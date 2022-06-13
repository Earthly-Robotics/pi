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
        
    def move_wheels(self, x, y):
        """
        Moves the wheels based on joystick position
        :param x: joystick x position
        :param y: joystick y position
        :return:
        """

        max_mid = 500  # Deadzone positive x and y
        min_mid = 400  # Deadzone negative x and y
        power_left = 0
        power_right = 0
        if min_mid < x < max_mid and min_mid < y < max_mid:
            power_left = 0
            power_right = 0

        # forwards
        if y > max_mid > x > min_mid:
            percent = math.floor(((y - max_mid) / 521) * 100)
            power_left = percent
            power_right = percent
            print("forwards")

        # backwards
        if y < min_mid < x < max_mid:
            percent = math.floor(((y - min_mid) / min_mid) * 100)
            power_left = percent
            power_right = percent
            print("backwards")

        # left
        if x < min_mid < y < max_mid:
            percent = math.floor(((x - min_mid) / min_mid) * 100) # negative number
            power_left = percent # negative
            power_right = -1 * percent # positive
            print("left")

        # right
        if x > max_mid > y > min_mid:
            percent = math.floor(((x - max_mid) / 521) * 100) # positive number
            power_left = percent # positive
            power_right = -1 * percent # negative
            print("right")

        # # top-right
        # elif x > max_mid and y > max_mid:
        #     print("top-right")
        #     percent = math.floor(((x - max_mid + y - max_mid) / 512) * 100)
        #     print(percent)
        #     self.power_left = 100
        #     self.power_right = 50
        #
        # # top-left
        # elif x < min_mid and y > max_mid:
        #     self.power_left = 100
        #     self.power_right = 50
        #     print("top-left")
        #
        # # bottom-right
        # elif x > max_mid and y < min_mid:
        #     self.power_left = 100
        #     self.power_right = 50
        #     print("bottom-right")
        #
        # # bottom-left
        # elif x < min_mid and y < min_mid:
        #     self.power_left = 100
        #     self.power_right = 50
        #     print("bottom-left")

        self.motor_left.move(power_left)
        self.motor_right.move(power_right)

# https://sensorkit.joy-it.net/en/sensors/ky-023
