import time


class DanceController:

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
        frequency = self.sound_controller.get_frequency()
        # bpm = self.sound_controller.bpm_count()
        print(frequency)
        if 60 < frequency < 201:
            if self.count < 10:
                self.wheels_controller.move(40, 0)
            if 10 < self.count < 21:
                self.wheels_controller.move(-40, 0)
            if self.count == 20:
                self.count = 0
            self.wheels_controller.move(0, 0)
            print("count: " + str(self.count))
        if 70 < frequency < 250:
            pass
            print("bass")
            # bass
        if 500 < frequency < 3500:
            pass
            print("harmonics")
            # harmonics
        if 200 < frequency < 2000:
            pass
            print("wheel_servos")
            # TODO: wheel servos
        if frequency > 2000:
            pass
            print("arm")
            # TODO: arm

        # tot 200, 2000, > 2000
        self.count = self.count + 1

        return self

    def solo_dance(self):
        self.msg_type = "SOLO_DANCE"

        print("Pick the robot up to adjust the wheel servos")
        input("Press Enter to continue when robot is picked up...")
        self.arduino_controller.send_message("left_wheel;-149")
        self.arduino_controller.send_message("right_wheel;-149")

        self.timeout_start = time.time()
        # arm move up and down for 5 seconds
        print(self.timeout_start)
        while time.time() < self.timeout_start + 5:
            # print("arm")
            i = 0
            #arm
            print(i)
            if i % 10 == 0:
                self.arduino_controller.send_message("arm;-140")
            if i % 5 == 0:
                self.arduino_controller.send_message("arm;-120")
            # self.wheels_controller.move(10, 0)

        # 10 seconde heen en weer
        # af en toe wiel servo's op en neer
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 10:
            i = 0

            #wheelservos
            if i % 10 == 0:
                self.wheels_controller.move(-100, 0, 4)
            if i % 5 == 0:
                self.wheels_controller.move(100, 0, 4)

        # tot 38 seconde armpie en wat bewegen
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 28:
            self.wheels_controller.move(-50, 0, 20)
            self.wheels_controller.move(50, 0, 20)

        # snel om as draaien op beat
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 42:
            self.wheels_controller.move(-100, 0, 2)
            self.wheels_controller.move(100, 0, 2)

        # vanaf 1:20, armpie weer
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 20:
            self.wheels_controller.move(-100, 0, 2)
            self.wheels_controller.move(100, 0, 2)
            #arm

        # vanaf 1:40, proberen twerken
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 13:
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
