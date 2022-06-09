import time
from ComponentControllers.WheelsController import WheelsController

#functies: vierkant rijden, rondje rijden, arduino servo start&stop

class AutoSeedPlant:

    def __init__(self):
        self.wheels_controller = WheelsController()

    def plantSeeds(self, form):
        match form:
            case "SQ":
                self.square()
            case "CI":
                self.circle()
            case "ST":
                self.straight()

    def straight(self):
        self.wheels_controller.goForward()

    def square(self):
        # To Do: forward, left, forward, left, forward, left, forward
        turns = 3
        self.wheels_controller.goForward()
        for x in range(turns):
            self.wheels_controller.goLeft()
            time.sleep(3)
            self.wheels_controller.goForward()
            time.sleep(5)

    def circle(self):
        #To Do: turn left and forward together
        self.wheels_controller.goLeftForward()
