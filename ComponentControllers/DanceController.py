import time


class DanceController:

    def __init__(self, sound_controller, wheels_controller):
        self.timeout_start = None
        self.sound_controller = sound_controller
        self.wheels_controller = wheels_controller
        self.network_controller = None
        self.listening = True
        self.count = 0

    def line_dance(self):
        """
        Starts linedancing
        :return:
        """
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
            #bass
        if 500 < frequency < 3500:
            pass
            print("harmonics")
            #harmonics
        if 200 < frequency < 2000:
            pass
            print("wheel_servos")
            #TODO: wheel servos
        if frequency > 2000:
            pass
            print("arm")
            #TODO: arm

# tot 200, 2000, > 2000
        self.count = self.count + 1

        return

    def solo_dance(self):
        #10 seconde heen en weer
        #af en toe wiel servo's op en neer
        #tot 38 seconde armpie en wat bewegen
        #snel om as draaien op beat
        #vanaf 1:20, armpie weer
        #vanaf 1:40, proberen twerken
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 5000:
            # arm move up and down for 5 seconds
            self.wheels_controller.move(1000, 0)
            
        self.timeout_start = time.time()
        while time.time() < self.timeout_start + 28000:
            self.wheels_controller.move(-20, 0)
            self.wheels_controller.move(20, 0)

        self.wheels_controller.move(-1000, 1000)


    def stop_sending(self):
        self.listening = False