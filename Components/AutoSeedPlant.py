from time import sleep
from ComponentControllers.WheelsController import WheelsController

#functies: vierkant rijden, rondje rijden, arduino servo start&stop

class AutoSeedPlant:

    def __init__(self):
        self.wheels_controller = WheelsController()

    def plantSeeds(self,rows,amount,sSpace,rSpace):
        # To Do: hoeken berekenen met gyroscoop, space berekenen per sec
        rows = rows
        amountseeds = amount
        seedspace = sSpace #space in seconds
        rowspace = rSpace #space in seconds
        for x in range(rows):
            for y in range(amountseeds):
                self.wheels_controller.goForward()
                sleep(seedspace)
                self.wheels_controller.stop()
                #do servo plant thingy

            #turn around
            if (x % 2) == 0:
                self.wheels_controller.goRight()
                self.wheels_controller.goForward()
                sleep(rowspace)
                self.wheels_controller.goRight()
                self.wheels_controller.stop()
            else:
                self.wheels_controller.goLeft()
                self.wheels_controller.goForward()
                sleep(rowspace)
                self.wheels_controller.goLeft()
                self.wheels_controller.stop()