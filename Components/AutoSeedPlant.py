import time
from ComponentControllers.WheelsController import WheelsController


class AutoSeedPlant:

    def __init__(self):
        self.wheels_controller = WheelsController()
        self.rows = 10
        self.distance_row = 5000;
        self.seed_per_row = 5;
        self.distance_between_row = 400;

    def find_blue_block(self):
        # TODO find blue block
        return

    def plant_seed(self):
        self.findBlueBlock()

        for x in range(self.rows):
            # Turn Right or Left, plant the seeds in the row, turn Right or Left again
            self.turn(x % 2 == 0)
            self.plant_seed()
            self.turn(x % 2 == 0)
            # Move distance_between_row
            cur_distance = 0
            while cur_distance < self.distance_between_row:
                self.wheels_controller.move(0, 100, 50)
                cur_distance += 1

            self.wheels_controller.stop()

    def plant_seed(self):
        # TODO plant seed funtion here
        for x in range(self.seed_per_row - 1):
            self.wheels_controller.move(0, 100, 50)
            cur_distance = 0
            while cur_distance < self.seed_per_row / self.distance_row:
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