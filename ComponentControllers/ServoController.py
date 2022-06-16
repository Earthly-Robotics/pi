from Utility import calculate_percentage


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

    def power_servo(self, y, string):
        result = calculate_percentage(y)

    def sendMessage(self, message):
        self.arduino_controller.send_message()