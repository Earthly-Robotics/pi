from Components.WheelMotor import WheelMotor


class WheelsController:
    wheels_left_names = ['wheel1', 'wheel4']
    wheels_left = []
    wheels_right_names = ['wheel2', 'wheel3']
    wheels_right = []

    def __init__(self):
        return

    def set_velocity(self, side, velocity):
        if side == "left":
            for i in range(len(self.wheels_left)):
                self.wheels_left[i].set_position(float('inf'))
                self.wheels_left[i].set_velocity(velocity)
        elif side == "right":
            for i in range(len(self.wheels_right)):
                self.wheels_right[i].set_position(float('inf'))
                self.wheels_right[i].set_velocity(velocity)
        elif side == "both":
            for i in range(len(self.wheels_right)):
                self.wheels_right[i].set_position(float('inf'))
                self.wheels_right[i].set_velocity(velocity)

            for i in range(len(self.wheels_left)):
                self.wheels_left[i].set_position(float('inf'))
                self.wheels_left[i].set_velocity(velocity)
        else:
            print("Did not set Velocity. Side was not 'left', 'right' or 'both'")