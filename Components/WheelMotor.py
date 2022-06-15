# from time import sleep, time
import threading
import time
import RPi.GPIO as GPIO


class WheelMotor:
    def __init__(self, forward, backward, pwm_pin):
        self.forward = forward
        self.backward = backward
        self.pwm_pin = pwm_pin
        self.last_percentage = 0
        self.direction = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.forward, GPIO.OUT)  # Connected to 19
        GPIO.setup(self.backward, GPIO.OUT)  # Connected to 16
        GPIO.setup(self.pwm_pin, GPIO.OUT)  # Connected to PWM
        self.pwm = GPIO.PWM(self.pwm_pin, 1000)  # Sets pwm frequency to 1000
        self.lock = threading.Lock()

    def move(self, power):
        """
        Moves motor based on power
        :param power: amount of power sent to motor (-100 to 100)
        :return:
        """

        self.pwm.start(abs(self.last_percentage))
        try:
            GPIO.output(self.forward, GPIO.LOW)  # Set AIN2
            GPIO.output(self.backward, GPIO.LOW)  # Set AIN2
            # print(power)
            if power > 0:
                self.direction = True
                if self.last_percentage < 0:
                    for i in range(abs(self.last_percentage), abs(power) - 1, -1):  # Loop 0 to 100 stepping dc by 5 each loop
                        self.pwm.ChangeDutyCycle(i)
                        GPIO.output(self.backward, GPIO.HIGH)
                    time.sleep(0.030)
                    for i in range(0, abs(power), 1):
                        self.pwm.ChangeDutyCycle(i)
                        GPIO.output(self.forward, GPIO.HIGH)
                else:
                    if power > self.last_percentage:
                        for i in range(self.last_percentage, abs(power), 1):  # Loop 0 to 100 stepping dc by 5 each loop
                            GPIO.output(self.forward, GPIO.HIGH)
                            self.pwm.ChangeDutyCycle(i)
                    elif power < self.last_percentage:
                        for i in range(self.last_percentage, abs(power) - 1, -1):  # Loop 0 to 100 stepping dc by 5 each loop
                            self.pwm.ChangeDutyCycle(i)
                            GPIO.output(self.forward, GPIO.HIGH)
                    else:
                        self.pwm.ChangeDutyCycle(power)
                        GPIO.output(self.forward, GPIO.HIGH)

            elif power < 0:
                self.direction = False
                if self.last_percentage > 0:
                    for i in range(abs(self.last_percentage), abs(power) - 1, -1):  # Loop 0 to 100 stepping dc by 5 each loop
                        self.pwm.ChangeDutyCycle(i)
                        GPIO.output(self.forward, GPIO.HIGH)
                    time.sleep(0.030)
                    for i in range(0, abs(power), 1):  # Loop 0 to 100 stepping dc by 5 each loop
                        self.pwm.ChangeDutyCycle(i)
                        GPIO.output(self.backward, GPIO.HIGH)
                else:
                    if power > abs(self.last_percentage):
                        for i in range(abs(self.last_percentage), abs(power), 1):  # Loop 0 to 100 stepping dc by 5 each loop
                            self.pwm.ChangeDutyCycle(i)
                            GPIO.output(self.backward, GPIO.HIGH)
                    else:
                        for i in range(abs(self.last_percentage), abs(power) - 1, -1):  # Loop 0 to 100 stepping dc by 5 each loop
                            self.pwm.ChangeDutyCycle(i)
                            GPIO.output(self.backward, GPIO.HIGH)
            else:
                if self.direction is True:
                    for i in range(abs(self.last_percentage), abs(power) - 1, -1):  # Loop 0 to 100 stepping dc by 5 each loop
                        self.pwm.ChangeDutyCycle(i)
                        GPIO.output(self.forward, GPIO.HIGH)
                else:
                    for i in range(abs(self.last_percentage), abs(power) - 1, -1):  # Loop 0 to 100 stepping dc by 5 each loop
                        self.pwm.ChangeDutyCycle(i)
                        GPIO.output(self.backward, GPIO.HIGH)
            self.lock.acquire()
            self.last_percentage = power
            self.lock.release()

            time.sleep(0.030)  # wait .001 seconds for timing

        except KeyboardInterrupt:
            self.pwm.stop()
            GPIO.cleanup()
