class WheelMotor:
    motor = None

    def __init__(self, robot, name):
        self.motor = robot.getDevice(name)

    def set_position(self, position):
        if self.motor is not None:
            self.motor.setPosition(position)
            return
        print("Could not set position. Motor is None.")

    def set_velocity(self, velocity):
        if self.motor is not None:
            self.motor.setVelocity(velocity)
            return
        print("Could not set velocity. Motor is None.")
