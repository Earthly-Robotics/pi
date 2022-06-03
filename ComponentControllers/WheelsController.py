from Components.WheelMotor import WheelMotor


class WheelsController:

    def move_logic(self, x, y):

        motor_left = WheelMotor(19, 16, 13)
        motor_right = WheelMotor(9, 10, 14)

        if 400 < x < 500 and 400 < y < 500:
            motor_left.move(0)
            motor_right.move(0)
        # forwards
        if y > 500 and x < 1010 and x > 100:
            motor_left.move(0.5)
            motor_right.move(0.5)
            print("forwards")

        # backwards
        if y < 400 and x < 1010 and x > 100:
            motor_left.move(0.5)
            motor_right.move(0.25)
            print("backwards")

        # left
        if x < 400 and y < 1010 and y > 100:
            motor_left.move(0.5)
            motor_right.move(0.5)
            print("left")

        # right
        if x > 500 and y < 1010 and y > 100:
            motor_left.move(0.5)
            motor_right.move(0.5)
            print("right")

        # top-right
        if x > 1010 and y > 1010:
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
        if x == 1 and y == 1010:
            motor_left.move(0.25)
            motor_right.move(0.5)
            print("top-left")

        # bottom-right
        if x > 1010 and y == 1:
            motor_left.move(0.25)
            motor_right.move(0.5)
            print("bottom-right")

        # bottom-left
        if x == 1 and y == 1:
            motor_left.move(0.5)
            motor_right.move(0.25)
            print("bottom-left")

        # https://sensorkit.joy-it.net/en/sensors/ky-023
