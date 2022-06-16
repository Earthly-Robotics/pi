import time
from ComponentControllers.WheelsController import WheelsController

#functies: vierkant rijden, rondje rijden, arduino servo start&stop

class AutoSeedPlant:

    def __init__(self):
        self.wheels_controller = WheelsController()

    def square(self):
        # To Do: forward, left, forward, left, forward, left, forward
        turns = 3
        self.wheels_controller.move_logic(205, 600)
        for x in range(turns):
            self.wheels_controller.move_logic(200,200)
            time.sleep(3)
            self.wheels_controller.move_logic(205, 505)
            time.sleep(5)

    def circle(self):
        #To Do: turn left and forward together
        self.wheels_controller.move_logic(205, 600)