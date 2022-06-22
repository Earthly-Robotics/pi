from time import sleep
from ComponentControllers.WheelsController import WheelsController
from Components.GyroAccelerometer import GyroAccelerometer
from ComponentControllers.ArduinoController import ArduinoController

#GYRO_YOUT_H  = 0x45

class AutoSeedPlant:

    def __init__(self):
        self.wheels_controller = WheelsController()
        self.gyro_accelerometer = GyroAccelerometer()
        self.arduino_controller = ArduinoController()

    def calcDist(self,dist):
        # To Do: calc distance in sec between rows & seeds , cm to sec?
        velocity = self.gyro_accelerometer.format_commponent_data()
        cms = velocity * 27.777778
        sec = 1/(cms/dist)
        return sec

    def plantSeeds(self,rows,amount,rSpace,sSpace):
        # To Do: space berekenen per sec
        rows = rows
        amountseeds = amount
        rowspace = self.calcDist(rSpace) #space in cm converted to sec
        seedspace = self.calcDist(sSpace)  # space in cm converted to sec

        for x in range(rows):
            for y in range(amountseeds):
                self.wheels_controller.go_forward()
                sleep(seedspace)
                self.wheels_controller.stop()
                #do servo plant thingy
                self.arduino_controller.send_message("hopperTimed")

            #turn around
            if (x % 2) == 0:
                self.turn90("RIGHT")
                self.wheels_controller.go_forward()
                sleep(rowspace)
                self.turn90("RIGHT")
                self.wheels_controller.stop()
            else:
                self.turn90("LEFT")
                self.wheels_controller.go_forward()
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
                    self.wheels_controller.turn_right()
                case "LEFT":
                    self.wheels_controller.turn_left()
            gyro_difference = self.getGyroDifference(start_gyro_y)
            if gyro_difference >= turn_degrees or gyro_difference >= turn_degrees * -1:
                break