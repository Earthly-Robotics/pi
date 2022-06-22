import time
from ComponentControllers.WheelsController import WheelsController


class AutoSeedPlant:

    def __init__(self):
        self.wheels_controller = WheelsController()
        self.planting = False

    def find_blue_block(self):
        # TODO find blue block
        return

    def plant_seed(self, rows, distance_row, seed_per_row, distance_between_row):
        self.findBlueBlock()
        for x in range(rows):
            # Turn Right or Left, plant the seeds in the row, turn Right or Left again
            self.turn(x % 2 == 0)
            self.plant_seed(distance_row, seed_per_row)
            self.turn(x % 2 == 0)
            # Move distance_between_row
            cur_distance = 0
            while cur_distance < distance_between_row:
                self.wheels_controller.move(0, 100, 50)
                cur_distance += 1

            self.wheels_controller.stop()

    def plant_seed(self, distance_row, seed_per_row):
        # TODO plant seed funtion here
        for x in range(seed_per_row - 1):
            self.wheels_controller.move(0, 100, 50)
            cur_distance = 0
            while cur_distance < seed_per_row / distance_row:
                self.wheels_controller.stop()
                cur_distance += 1
            # TODO plant seed funtion here

    def turn(self, right):
        if right:
            self.wheels_controller.turn_right(50)
            cur_distance = 0
            while cur_distance < 800:
                self.wheels_controller.stop()
                cur_distance += 1
            self.wheels_controller.stop()
        else:
            self.wheels_controller.turn_left(50)
            cur_distance = 0
            while cur_distance < 800:
                self.wheels_controller.stop()
                cur_distance += 1
            self.wheels_controller.stop()