from time import sleep
from ComponentControllers.WheelsController import WheelsController
from Components.GyroAccelerometer import GyroAccelerometer

GYRO_YOUT_H  = 0x45

class AutoSeedPlant:

    def __init__(self):
        self.wheels_controller = WheelsController()
        self.gyro_accelerometer = GyroAccelerometer()

    def findStartPos(self):
        # To Do: find start pos with blue block
        pass

    def plantSeeds(self,rows,amount,rSpace,sSpace):
        # To Do: hoeken berekenen met gyroscoop, space berekenen per sec, find startplace with blueblock
        rows = rows
        amountseeds = amount
        rowspace = rSpace #space in seconds
        seedspace = sSpace  # space in seconds

        for x in range(rows):
            for y in range(amountseeds):
                self.wheels_controller.goForward()
                sleep(seedspace)
                self.wheels_controller.stop()
                #do servo plant thingy

            #turn around
            if (x % 2) == 0:
                self.turn90("RIGHT")
                self.wheels_controller.goForward()
                sleep(rowspace)
                self.turn90("RIGHT")
                self.wheels_controller.stop()
            else:
                self.turn90("LEFT")
                self.wheels_controller.goForward()
                sleep(rowspace)
                self.turn90("LEFT")
                self.wheels_controller.stop()

    def getGyroDifference(self, start_gyro):
        start_gyro = start_gyro
        current_gyro_y = abs(float(GyroAccelerometer.get_gyro_data()["y"])) #get gyro y data
        return start_gyro - current_gyro_y

    def turn90(self,direction):
        start_gyro_y = abs(float(GyroAccelerometer.get_gyro_data()["y"]))  # get start gyro y data
        turn_degrees = 90

        while True:
            match (direction):
                case "RIGHT":
                    self.wheels_controller.goRight()
                case "LEFT":
                    self.wheels_controller.goLeft()
            gyro_difference = self.getGyroDifference(start_gyro_y)
            if gyro_difference >= turn_degrees or gyro_difference >= turn_degrees * -1: 
                break