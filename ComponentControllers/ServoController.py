import math


class ServoController:

# initialise the servos that need to work on joysticks
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

# put servo in list
    servo_list = [arm, wiel1, wiel2]

# standard values
    def __init__(self, arduino_controller):
        self.arduino_controller = arduino_controller
        self.max_degrees = 150
        self.min_degrees = -150

# function to open and close magnet
    def control_magnet(self, magnet_status):
        if magnet_status == False:
            magnet_status = True
            self.arduino_controller.send_message("magnet;30")
        else:
            magnet_status = False
            self.arduino_controller.send_message("magnet;-30")

# private function to calculate how much precent the joystick is giving off
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

# power the servo based on the percentage
    def power_servo(self, y, profile):
        result = self.calculate_percentage(y)
# profile 0 is to control the wheel servos
        if profile == 0:

            # vanwege tandwielen x2
            power = result/30
            current_deg = self.servo_list[1]
            new_degrees = (current_deg["POS"] + power)*2
            current_deg["POS"] = new_degrees
            # to prevent the servo to spin into the deathzone there's a limit
            if(new_degrees < 150 and new_degrees > -150):
                # send string to arduino
                self.arduino_controller.send_message(str.format("{0};{1}", current_deg["ID"], current_deg["POS"]))

                current_deg = self.servo_list[2]
                new_degrees * -1
                current_deg["POS"] = new_degrees
                # send string to arduino
                self.arduino_controller.send_message(str.format("{0};{1}", current_deg["ID"], current_deg["POS"]))


# profile 1 is to control the arm servo
        elif profile == 1:
            power = result / 30
            current_deg = self.servo_list[0]
            new_degrees = current_deg["POS"] + power
            current_deg["POS"] = new_degrees
            # to prevent the servo to spin into the deathzone there's a limit
            if (new_degrees < 150 and new_degrees > -150):
                # send string to arduino
                self.arduino_controller.send_message(current_deg["ID"] + ";" + current_deg["POS"])