from time import sleep

import gpiozero as GPIO


class WheelMotor:
    def __init__(self, forward, backward, pwm):
        self.motor = GPIO.Motor(forward, backward, pwm=False)
        self.pwm_out = GPIO.PWMOutputDevice(pwm)
        self.pwm_out.on()

    def move(self, power):
        if power > 0:
            self.motor.forward()
            print("Power:" + str(power))
        elif power < 0:
            self.motor.backward()
            print("Power:" + str(power))
        else:
            print("Power:" + str(power))
        self.pwm_out.value = abs(power)
        sleep(1)

