import time
from ComponentControllers.WheelsController import WheelsController
from Logger.ConsoleLogger import ConsoleLogger


class AutoSeedPlant:

    def __init__(self, wheels_controller=None, arduino_controller=None):
        self.wheels_controller = wheels_controller
        self.arduino_controller = arduino_controller
        self.logger = ConsoleLogger()
        self.stop = 20
        self.planting = False

    def find_blue_block(self):
        # TODO find blue block
        return

    def plant_seed(self, rows, distance_row, seed_per_row, distance_between_row, corner_distance):
        #self.findBlueBlock()
        for x in range(rows):
            # Turn Right or Left, plant the seeds in the row, turn Right or Left again
            self.turn(corner_distance, x % 2 == 0)
            self.plant_row_seed(distance_row, seed_per_row)
            self.turn(corner_distance, x % 2 == 1)
            # Move distance_between_row
            for y in range(int(distance_between_row / 4)):
                self.wheels_controller.move(0, 100, 2)
            for y in range(self.stop):
                self.wheels_controller.stop()

    def plant_row_seed(self, distance_row, seed_per_row):
        self.arduino_controller.send_message("hopper;490")
        for y in range(self.stop * 2):
            self.wheels_controller.stop()
        for x in range(seed_per_row - 1):
            for y in range(int(int(distance_row / 4) / (seed_per_row - 1))):
                self.wheels_controller.move(0, 100, 2)
            for y in range(self.stop):
                self.wheels_controller.stop()
            self.arduino_controller.send_message("hopper;490")
            for y in range(self.stop * 2):
                self.wheels_controller.stop()

    def turn(self, corner_distance, right):
        if right:
            for x in range(corner_distance):
                self.wheels_controller.turn_right(50)
            for x in range(self.stop):
                self.wheels_controller.stop()
        else:
            for x in range(corner_distance):
                self.wheels_controller.turn_left(50)
            for x in range(self.stop):
                self.wheels_controller.stop()

    def stop_sending(self):
        self.planting = False