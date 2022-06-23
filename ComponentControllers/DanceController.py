import threading
import time


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

    def line_dance(self):
        """
        Starts linedancing
        :return:
        """
        self.msg_type = "LINE_DANCE"

        print("Pick the robot up to adjust the wheel servos")
        input("Press Enter to continue when robot is picked up...")
        time.sleep(1)
        # self.arduino_controller.send_message("left_wheel;-120~right_wheel;-120")
        time.sleep(1)
        print("Done! Starting in 3 seconds...")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")

        while self.sending:
            frequency = self.sound_controller.get_frequency()
            # bpm = self.sound_controller.bpm_count()
            print(frequency)
            # if 60 < frequency < 201:

            if 70 < frequency < 250:
                # bass
                time.sleep(.002)
                self.arduino_controller.send_message("arm;-140~")
                time.sleep(.002)
                self.arduino_controller.send_message("arm;-30~")
            if 500 < frequency < 3500:
                # harmonics
                if self.count < 10:
                    self.wheels_controller.move(100, 0, 4)
                if 10 < self.count < 21:
                    self.wheels_controller.move(-100, 0, 4)

                print("count: " + str(self.count))

                # wheel servos
                if 15 < self.count < 30:
                    time.sleep(0.002)
                    self.arduino_controller.send_message("left_wheel;-100~")
                    self.arduino_controller.send_message("right_wheel;-120~")
                    time.sleep(0.002)
                    self.arduino_controller.send_message("left_wheel;-120~")
                    self.arduino_controller.send_message("right_wheel;-100~")
                if self.count == 20:
                    self.count = 0
                self.count = self.count + 1

            if frequency > 3500:
                # arm
                time.sleep(.002)
                self.arduino_controller.send_message("arm;-140~")
                time.sleep(.002)
                self.arduino_controller.send_message("arm;-30~")

            # tot 200, 2000, > 2000

        return self

    def solo_dance(self):
        self.msg_type = "SOLO_DANCE"
        self.count = 0

        print("Pick the robot up to adjust the wheel servos")
        input("Press Enter to continue when robot is picked up...")
        time.sleep(1)
        # self.arduino_controller.send_message("left_wheel;-120~right_wheel;-120")
        time.sleep(1)
        print("Done! Starting in 3 seconds...")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        self.timeout_start = time.time()
        # arm move up and down for 5 seconds
        print(self.timeout_start)
        while time.time() < self.timeout_start + 5:
            # print("arm")
            #arm
            time.sleep(.0002)
            self.arduino_controller.send_message("arm;-140~")
            time.sleep(.002)
            self.arduino_controller.send_message("arm;-80~")
            time.sleep(.0002)
            self.arduino_controller.send_message("arm;-30~")

        # 10 seconde heen en weer
        # af en toe wiel servo's op en neer
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 10:
            #wheelservos
            time.sleep(0.02)
            self.arduino_controller.send_message("left_wheel;-90~")
            self.arduino_controller.send_message("right_wheel;-120~")
            time.sleep(0.02)
            self.arduino_controller.send_message("left_wheel;-120~")
            self.arduino_controller.send_message("right_wheel;-90~")

            print(self.count)
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

            self.arduino_controller.send_message("arm;-140~")
            time.sleep(.02)
            self.arduino_controller.send_message("arm;-80~")
            time.sleep(.02)
            self.arduino_controller.send_message("arm;-30~")

        # snel om as draaien op beat
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 42:
            if self.count < 50:
                self.wheels_controller.move(-100, 0, 2)
            elif 49 < self.count < 100:
                self.wheels_controller.move(100, 0, 2)
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
            time.sleep(0.02)
            print("arm -140")
            self.arduino_controller.send_message("arm;-140")
            time.sleep(0.02)
            print("arm -120")
            self.arduino_controller.send_message("arm;-120")

        # vanaf 1:40, proberen twerken
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 13:
            time.sleep(0.02)
            self.arduino_controller.send_message("left_wheel;-80~")
            self.arduino_controller.send_message("right_wheel;-120~")
            time.sleep(0.02)
            self.arduino_controller.send_message("left_wheel;-120~")
            self.arduino_controller.send_message("right_wheel;-80~")
            pass
            #twerk



        return self

    def stop_sending(self):
        #nick vragen voor de stop_sending
        self.sound_controller.stop_sending()
        self.wheels_controller.stop()
        # self.servo_controller.stop_sending()
        self.sending = False
        return self
