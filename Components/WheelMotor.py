# from time import sleep, time
import threading
import time
import RPi.GPIO as GPIO


class WheelMotor:
    def __init__(self, forward, backward, pwm):
        self.forward = forward
        self.backward = backward
        self.pwm = pwm
        self.last_percentage = 0
        self.lock = threading.Lock()

    def move(self, power):
        """
        Moves motor based on power
        :param power: amount of power sent to motor (-100 to 100)
        :return:
        """

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.forward, GPIO.OUT)  # Connected to 19
        GPIO.setup(self.backward, GPIO.OUT)  # Connected to 16
        GPIO.setup(self.pwm, GPIO.OUT)  # Connected to PWM
        pwm = GPIO.PWM(self.pwm, 2000)  # Sets pwm frequency to 1000

        pwm.start(self.last_percentage)
        # TODO: self.last_percentage wordt niet aangepast, waardoor hij het niet goed doet.
        try:
            GPIO.output(self.forward, GPIO.LOW)  # Set AIN2
            GPIO.output(self.backward, GPIO.LOW)  # Set AIN2
            # print(power)
            if power > 0:
                for i in range(self.last_percentage, power, 5):  # Loop 0 to 100 stepping dc by 5 each loop
                    pwm.ChangeDutyCycle(abs(i))
                    GPIO.output(self.forward, GPIO.HIGH)
            elif power < 0:
                for i in range(self.last_percentage, power, -5):  # Loop 0 to 100 stepping dc by 5 each loop
                    pwm.ChangeDutyCycle(abs(i))
                    GPIO.output(self.backward, GPIO.HIGH)
            self.lock.acquire()
            self.last_percentage = power
            self.lock.release()
            # TODO: brake, high both

            time.sleep(0.030)  # wait .001 seconds for timing

        except KeyboardInterrupt:
            pwm.stop()
            GPIO.cleanup()
        finally:
            pwm.stop()
            GPIO.cleanup()
