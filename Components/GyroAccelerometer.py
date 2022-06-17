import math

from mpu6050 import mpu6050
from Components.AppComponent import AppComponent


class GyroAccelerometer(AppComponent):
    initial_velocity = 0
    velocity = 0

    def __init__(self, network_controller):
        super().__init__(network_controller)
        self.msg_type = "VELOCITY"
        try:
            self.sensor = mpu6050(0x68)
            self.sensor.set_accel_range(self.sensor.ACCEL_RANGE_2G)
        except Exception as e:
            print("Could not connect to the mpu6050:\n", e)

    def get_accel_data(self):
        return self.sensor.get_accel_data()

    def get_gyro_data(self):
        return self.sensor.get_gyro_data()

    def format_component_data(self) -> tuple:
        """
        Gets the data from the component and formats it for JSON Serialization.
        :return:
        A tuple with an even amount of elements.
        Must be formatted as followed: "x", "x_value".
        """
        data = self.get_accel_data()
        vel_x = self.initial_velocity + abs(float(data["x"])) * self.interval
        vel_y = self.initial_velocity + abs(float(data["y"])) * self.interval
        vel_z = self.initial_velocity + abs(float(data["z"])) * self.interval
        self.velocity = ((vel_x + vel_y + vel_z) - 9.81) / (self.interval * 3)
        return "Velocity", str(round(self.velocity * 3.6, 2)) + " km/h"
