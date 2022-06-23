import threading
import time

from RepeatedTimer import RepeatedTimer


class DanceController:
    threads = list()

    def __init__(self, sound_controller, wheels_controller, arduino_controller):
        self.msg_type = "DANCE"

        self.timeout_start = None
        self.sound_controller = sound_controller
        self.wheels_controller = wheels_controller
        self.arduino_controller = arduino_controller
        self.network_controller = None
        self.sending = False
        self.count = 0
        self.once = 0

    def line_dance(self):
        """
        Starts linedancing
        :return:
        """
        self.msg_type = "LINE_DANCE"

        print("Pick the robot up to adjust the wheel servos")
        input("Press Enter to continue when robot is picked up...")
        time.sleep(1)
        self.arduino_controller.send_message("left_wheel;-120~right_wheel;-120")
        time.sleep(1)
        print("Done! Starting in 3 seconds...")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")

        while self.sending:
            frequency = self.sound_controller.get_frequency()
            # bpm = self.sound_controller.bpm_count()
            # if 60 < frequency < 201:

            if 70 < frequency < 250:
                # bass
                rt = RepeatedTimer(0.05, self.arduino_controller.send_message, "arm;-140~")
                try:
                    time.sleep(0.0002)  # your long-running job goes here...
                finally:
                    rt.stop()
                rt = RepeatedTimer(0.05, self.arduino_controller.send_message, "arm;-30~")
                try:
                    time.sleep(0.002)  # your long-running job goes here...
                finally:
                    rt.stop()
            if 500 < frequency < 3500:
                # harmonics
                if self.count < 10:
                    self.wheels_controller.move(100, 0, 3)
                if 10 < self.count < 21:
                    self.wheels_controller.move(-100, 0, 3)

                if self.count == 20:
                    self.count = 0
                self.count = self.count + 1

            rt = RepeatedTimer(0.02, self.arduino_controller.send_message, "arm;-120")
            try:
                time.sleep(0.02)  # your long-running job goes here...
            finally:
                rt.stop()
            rt = RepeatedTimer(0.02, self.arduino_controller.send_message, "arm;-30")
            try:
                time.sleep(0.02)  # your long-running job goes here...
            finally:
                rt.stop()

            # wheel servos
            if 15 < self.count < 20:
                rt = RepeatedTimer(0.02, self.arduino_controller.send_message, "left_wheel;-80~right_wheel;-120~")
                try:
                    time.sleep(0.02)  # your long-running job goes here...
                finally:
                    rt.stop()
                rt = RepeatedTimer(0.02, self.arduino_controller.send_message, "left_wheel;-120~right_wheel;-80~")
                try:
                    time.sleep(0.02)  # your long-running job goes here...
                finally:
                    rt.stop()
            # tot 200, 2000, > 2000

        return self

    def solo_dance(self):
        self.msg_type = "SOLO_DANCE"
        self.count = 0

        print("Pick the robot up to adjust the wheel servos")
        input("Press Enter to continue when robot is picked up...")
        time.sleep(1)
        self.arduino_controller.send_message("left_wheel;-120~right_wheel;-120")
        time.sleep(1)
        print("Done! Starting in 3 seconds...")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        self.timeout_start = time.time()
        # arm move up and down for 5 seconds
        while time.time() < self.timeout_start + 5:
            # print("arm")
            #arm
            rt = RepeatedTimer(0.05, self.arduino_controller.send_message, "arm;-140~")
            try:
                time.sleep(0.0002)  # your long-running job goes here...
            finally:
                rt.stop()
            rt = RepeatedTimer(0.05, self.arduino_controller.send_message, "arm;-80~")
            try:
                time.sleep(0.002)  # your long-running job goes here...
            finally:
                rt.stop()
            rt = RepeatedTimer(0.05, self.arduino_controller.send_message, "arm;-30~")
            try:
                time.sleep(0.002)  # your long-running job goes here...
            finally:
                rt.stop()

        # 10 seconde heen en weer
        # af en toe wiel servo's op en neer
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 10:
            #wheelservos
            rt = RepeatedTimer(0.05, self.arduino_controller.send_message, "left_wheel;-60~right_wheel;-120~")
            try:
                time.sleep(0.02)  # your long-running job goes here...
            finally:
                rt.stop()

            rt = RepeatedTimer(0.05, self.arduino_controller.send_message, "left_wheel;-120~right_wheel;-60~")
            try:
                time.sleep(0.02)  # your long-running job goes here...
            finally:
                rt.stop()

            if self.count < 15:
                self.wheels_controller.move(-100, 0, 4)
            elif 14 < self.count < 30:
                self.wheels_controller.move(100, 0, 4)
            else:
                self.count = 0
            self.count = self.count + 1

        # tot 38 seconde armpie en wat bewegen
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 28:
            if self.count < 50:
                self.wheels_controller.move(-100, 0, 3)
            elif 50 < self.count < 100:
                self.wheels_controller.move(100, 0, 3)
            else:
                self.count = 0
            self.count = self.count + 1

            rt = RepeatedTimer(0.02, self.arduino_controller.send_message, "arm;-140~")
            try:
                time.sleep(0.02)  # your long-running job goes here...
            finally:
                rt.stop()

            rt = RepeatedTimer(0.02, self.arduino_controller.send_message, "arm;-80~")
            try:
                time.sleep(0.02)  # your long-running job goes here...
            finally:
                rt.stop()

            rt = RepeatedTimer(0.02, self.arduino_controller.send_message, "arm;-30~")
            try:
                time.sleep(0.02)  # your long-running job goes here...
            finally:
                rt.stop()

        # snel om as draaien op beat
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 42:
            rt = RepeatedTimer(0.02, self.arduino_controller.send_message, "back_wheel;90")
            try:
                time.sleep(0.02)  # your long-running job goes here...
            finally:
                rt.stop()
            if self.count < 25:
                self.wheels_controller.move(-100, 0, 1)
            elif 24 < self.count < 50:
                self.wheels_controller.move(100, 0, 1)
            elif 49 < self.count < 60:
                rt = RepeatedTimer(1, self.arduino_controller.send_message, "back_wheel;0")
                try:
                    time.sleep(0.02)  # your long-running job goes here...
                finally:
                    rt.stop()
                self.wheels_controller.move(0, 100, 4)
            elif 59 < self.count < 60:
                self.wheels_controller.move(0, -100, 4)
            else:
                self.count = 0
            self.count = self.count + 1

        # vanaf 1:20, armpie weer
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 20:
            if self.count < 50:
                self.wheels_controller.move(-100, 0, 2)
            elif 49 < self.count < 100:
                self.wheels_controller.move(100, 0, 2)
            else:
                self.count = 0
            self.count = self.count + 1

            #arm
            rt = RepeatedTimer(0.02, self.arduino_controller.send_message, "arm;-140~")
            try:
                time.sleep(0.02)  # your long-running job goes here...
            finally:
                rt.stop()

            rt = RepeatedTimer(0.02, self.arduino_controller.send_message, "arm;-120~")
            try:
                time.sleep(0.02)  # your long-running job goes here...
            finally:
                rt.stop()

        # vanaf 1:40, proberen twerken
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 13:
            if self.count < 50:
                self.wheels_controller.move(-100, 0, 4)
            elif 49 < self.count < 100:
                self.wheels_controller.move(100, 0, 4)
            else:
                self.count = 0
            self.count = self.count + 1

            if self.once == 0:
                self.arduino_controller.send_message("left_wheel;0~right_wheel;-120~")
            rt = RepeatedTimer(0.02, self.arduino_controller.send_message, "right_wheel;-120~")
            try:
                time.sleep(0.05)  # your long-running job goes here...
            finally:
                rt.stop()

            rt = RepeatedTimer(0.002, self.arduino_controller.send_message, "right_wheel;-60~")
            try:
                time.sleep(0.05)  # your long-running job goes here...
            finally:
                rt.stop()
            self.once = self.once + 1
        print("Dance is finished, going down in 3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        self.arduino_controller.send_message("left_wheel;0~right_wheel;0~")


        return self

    def stop_sending(self):
        #nick vragen voor de stop_sending
        self.sound_controller.stop_sending()
        self.wheels_controller.stop()
        # self.servo_controller.stop_sending()
        self.sending = False
        return self
