import time
from time import sleep
from ComponentControllers.WheelsController import WheelsController
from Components.GyroAccelerometer import GyroAccelerometer
from ComponentControllers.ArduinoController import ArduinoController

#GYRO_YOUT_H  = 0x45

class AutoSeedPlant:

    def __init__(self, network_controller, wheels_controller, gyro_accelerometer, arduino_controller):
        self.wheels_controller = wheels_controller
        self.gyro_accelerometer = gyro_accelerometer
        self.arduino_controller = arduino_controller

    # calc distance in sec between rows & seeds , cm to sec
    def calc_dist(self, dist):
        velocity = self.gyro_accelerometer.calculate_velocity() *3.6
        cms = abs(float(velocity) * 27.777778)
        sec = 1/(cms/dist)
        return sec

    # plant seeds in grid
    def plant_seeds(self, rows, amount, r_space, s_space):
        rows = rows
        amount_seeds = amount
        row_space = self.calc_dist(r_space) # space in cm converted to sec
        seed_space = self.calc_dist(s_space)  # space in cm converted to sec

        for x in range(rows):
            for y in range(amount_seeds):
                self.wheels_controller.go_forward()
                sleep(seed_space)
                self.wheels_controller.stop()
                # do servo plant thingy
                self.arduino_controller.send_message("hopper")
                time.sleep(2)
            # turn around
            if (x % 2) == 0:
                self.turn90("RIGHT")
                self.wheels_controller.go_forward()
                sleep(row_space)
                self.turn90("RIGHT")
                self.wheels_controller.stop()
            else:
                self.turn90("LEFT")
                self.wheels_controller.go_forward()
                sleep(row_space)
                self.turn90("LEFT")
                self.wheels_controller.stop()

    # get amount rotated
    def get_gyro_difference(self, start_gyro):
        start_gyro = start_gyro
        current_gyro_y = abs(float(self.gyro_accelerometer.get_gyro_data()["y"])) #get gyro y data
        return start_gyro - current_gyro_y

    # turn 90 degrees left or right
    def turn90(self, direction):
        start_gyro_y = abs(float(self.gyro_accelerometer.get_gyro_data()["y"]))  # get start gyro y data
        turn_degrees = 90

        while True:
            match (direction):
                case "RIGHT":
                    self.wheels_controller.turn_right()
                case "LEFT":
                    self.wheels_controller.turn_left()
            gyro_difference = self.get_gyro_difference(start_gyro_y)
            if gyro_difference >= turn_degrees or gyro_difference >= turn_degrees * -1:
                break