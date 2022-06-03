from WheelMotor import *
from time import sleep
import gpiozero as GPIO


class WheelsController:
    # def __init__(self):

    def move_logic(self, cmd):

        motor_left = WheelMotor( 19, 16, 13)
        # 13 PWM
        motor_right = WheelMotor(9, 10, 14)


        # forwards
        if cmd.joystick_position_y == 1 and cmd.joystick_position_x < 1010 and cmd.joystick_position_x > 100:
            motor_left.move(0.5)
            motor_right.move(0.5)

            sleep(5)
            print("forwards")

        # backwards
        if cmd.joystick_position_y > 1010 and cmd.joystick_position_x < 1010 and cmd.joystick_position_x > 100:
            motor_left.move(0.5)
            motor_right.move(0.25)

            sleep(5)
            print("backwards")

        # left
        if cmd.joystick_position_x == 1 and cmd.joystick_position_y < 1010 and cmd.joystick_position_y > 100:
            motor_left.move(0.5)
            motor_right.move(0.5)

            sleep(5)
            print("left")

        # right
        if cmd.joystick_position_x > 1010 and cmd.joystick_position_y < 1010 and cmd.joystick_position_y > 100:
            motor_left.move(0.5)
            motor_right.move(0.5)
            sleep(5)
            print("right")

        #top-right
        if cmd.joystick_position_x > 1010 and cmd.joystick_position_y == 1:
            print("top-right")
            # motor_left.move(0.2)
            # motor_left.move(0.4)
            # motor_left.move(0.6)
            # motor_left.move(0.8)
            # motor_left.move(1)
            # motor_left.move(0.9)
            # motor_left.move(0.6)
            # motor_left.move(0.4)
            # motor_left.move(0.2)
            # sleep(2)
            # motor_left.move(0)
            # sleep(2)
            # motor_left.move(-0.2)
            # motor_left.move(-0.5)
            # motor_left.move(-0.8)
            # motor_left.move(-1)
            motor_left.move(0.5)
            motor_right.move(0.25)

        #top-left
        if cmd.joystick_position_x == 1 and cmd.joystick_position_y == 1:
            motor_left.move(0.25)
            motor_right.move(0.5)

            sleep(5)
            print("top-left")

        #bottom-right
        if cmd.joystick_position_x > 1010 and cmd.joystick_position_y > 1010:
            motor_left.move(0.25)
            motor_right.move(0.5)

            sleep(5)
            print("bottom-right")

        #bottom-left
        if cmd.joystick_position_x == 1 and cmd.joystick_position_y > 1010:
            motor_left.move(0.5)
            motor_right.move(0.25)

            sleep(5)
            print("bottom-left")

        # https://sensorkit.joy-it.net/en/sensors/ky-023

