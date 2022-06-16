import math


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
        if magnet_status == False:
            magnet_status = True
            self.arduino_controller.send_message("magnet;30")
        else:
            magnet_status = False
            self.arduino_controller.send_message("magnet;-30")

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

            # vanwege tandwielen x2
            power = result/30
            current_deg = self.servo_list[1]
            new_degrees = (current_deg["POS"] + power)*2
            current_deg["POS"] = new_degrees
            if(new_degrees < 150 and new_degrees > -150):
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
            if (new_degrees < 150 and new_degrees > -150):
                self.arduino_controller.send_message(current_deg["ID"] + ";" + current_deg["POS"])