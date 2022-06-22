from Utility import calculate_percentage


class ServoController:

    arm = {
        "ID": "onderarm",
        "POS": 150
    }
    wiel1 = {
        "ID": "wiel1",
        "POS": 150
    }
    wiel2 = {
        "ID": "wiel2",
        "POS": 150
    }

    servo_list = [arm, wiel1, wiel2]

    def __init__(self, arduino_controller):
        self.arduino_controller = arduino_controller
        self.max_degrees = 150
        self.min_degrees = -150

    def control_magnet(self, magnet_status):
        if self.arduino_controller is None:
            return
        if magnet_status is False:
            magnet_status = True
            self.arduino_controller.send_message("magnet;30")
        else:
            magnet_status = False
            self.arduino_controller.send_message("magnet;-30")

    def power_servo(self, y, profile):
        if self.arduino_controller is None:
            return
        result = calculate_percentage(y)
        if profile == 0:

            # vanwege tandwielen x2
            power = result/30
            current_deg = self.servo_list[1]
            new_degrees = (current_deg["POS"] + power)*2
            current_deg["POS"] = new_degrees
            if 150 > new_degrees > -150:
                self.arduino_controller.send_message(str.format("{0};{1}", current_deg["ID"], current_deg["POS"]))

                current_deg = self.servo_list[2]
                new_degrees * -1
                current_deg["POS"] = new_degrees
                self.arduino_controller.send_message(str.format("{0};{1}", current_deg["ID"], current_deg["POS"]))

        elif profile == 1:
            power = result / 30
            current_deg = self.servo_list[0]
            new_degrees = current_deg["POS"] + power
            current_deg["POS"] = new_degrees
            if 150 > new_degrees > -150:
                self.arduino_controller.send_message(current_deg["ID"] + ";" + current_deg["POS"])

    def send_message(self, message):
        if self.arduino_controller is None:
            return
        self.arduino_controller.send_message(message)
