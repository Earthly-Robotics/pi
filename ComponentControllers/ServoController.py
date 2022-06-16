import math


class ServoController:

    def __init__(self, arduino_controller):
        self.arduino_controller = arduino_controller
        self.max_degrees = 150
        self.min_degrees = -150

    def control_magnet(self, magnet_status):
        if magnet_status == False:
            magnet_status = True
            self.arduino_controller.send_message("magneet;30")
        else:
            magnet_status = False
            self.arduino_controller.send_message("magneet;-30")

    def __calculate_percentage(self, y):
        # forwards
        if y > 0 and y <= 2047:
            percentage_pos = math.floor(((y) / 2047) * 100)
            output = math.floor((percentage_pos))

        # backwards
        elif y < -400 and y >= -2047:
            percentage_pos = math.floor(((y + 400) / 1647) * 100)
            output = math.floor((percentage_pos))

            return output

    def power_servo(self, y, profile):
        result = self.calculate_percentage(y)
        if profile == 0:
            pass  # vanwege tandwielen x2