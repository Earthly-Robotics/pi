from Components.WheelMotor import WheelMotor


class WheelsController:

    def move_logic(self, x, y):

        motor_left = WheelMotor(19, 16, 13)
        motor_right = WheelMotor(9, 10, 14)
        max_mid = 500
        min_mid = 400

        if min_mid < x < max_mid and min_mid < y < max_mid:
            motor_left.move(0)
            motor_right.move(0)
        # forwards
        if y > max_mid > x > min_mid:
            motor_left.move(0.5)
            motor_right.move(0.5)
            print("forwards")

        # backwards
        if y < min_mid < x < max_mid:
            motor_left.move(0.5)
            motor_right.move(0.25)
            print("backwards")

        # left
        if x < min_mid < y < max_mid:
            motor_left.move(0.5)
            motor_right.move(0.5)
            print("left")

        # right
        if x > max_mid > y > min_mid:
            motor_left.move(0.5)
            motor_right.move(0.5)
            print("right")

        # top-right
        if x > max_mid and y > max_mid:
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

        # top-left
        if x < min_mid and y > max_mid:
            motor_left.move(0.25)
            motor_right.move(0.5)
            print("top-left")

        # bottom-right
        if x > max_mid and y < min_mid:
            motor_left.move(0.25)
            motor_right.move(0.5)
            print("bottom-right")

        # bottom-left
        if x < min_mid and y < min_mid:
            motor_left.move(0.5)
            motor_right.move(0.25)
            print("bottom-left")

        # https://sensorkit.joy-it.net/en/sensors/ky-023
