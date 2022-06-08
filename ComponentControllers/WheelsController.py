from Components.WheelMotor import WheelMotor
from time import sleep
import math


class WheelsController:

    def move_wheels(self, x, y):
        """
        Moves the wheels based on joystick position
        :param x: joystick x position
        :param y: joystick y position
        :return:
        """

        motor_left = WheelMotor(19, 16, 13)
        motor_right = WheelMotor(9, 10, 14)
        max_mid = 500  # Deadzone positive x and y
        min_mid = 400  # Deadzone negative x and y

        if min_mid < x < max_mid and min_mid < y < max_mid:
            motor_left.move(0)
            motor_right.move(0)

        # forwards
        if y > max_mid > x > min_mid:
            percent = math.floor(((y - max_mid) / 521) * 100)
            # motor_left.move(min(min(percent, 100), 0))
            motor_left.move(percent)
            print("forwards")

        # backwards
        if y < min_mid < x < max_mid:
            percent = math.floor(((y - min_mid) / min_mid) * 100)
            motor_left.move(percent)
            motor_right.move(percent)
            print("backwards")

        # left
        if x < min_mid < y < max_mid:
            percent = math.floor(((x - min_mid) / min_mid) * 100)
            motor_left.move(percent)
            motor_right.move(percent)
            print("left")

        # right
        if x > max_mid > y > min_mid:
            percent = math.floor(((x - max_mid) / 521) * 100)
            motor_left.move(percent)
            motor_right.move(percent)
            print("right")


        """
        # top-right
        if x > max_mid and y > max_mid:
            print("top-right")
            motor_left.move(percent)
            motor_right.move(percent)

        # top-left
        if x < min_mid and y > max_mid:
            motor_left.move(percent)
            motor_right.move(percent)
            print("top-left")

        # bottom-right
        if x > max_mid and y < min_mid:
            motor_left.move(percent)
            motor_right.move(percent)
            print("bottom-right")

        # bottom-left
        if x < min_mid and y < min_mid:
            motor_left.move(percent)
            motor_right.move(percent)
            print("bottom-left")
        """
        # https://sensorkit.joy-it.net/en/sensors/ky-023
