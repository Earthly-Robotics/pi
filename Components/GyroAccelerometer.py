import smbus  # import SMBus module of I2C
from time import sleep  # import
class GyroAccelerometer:
    # some MPU6050 Registers and their Address
    PWR_MGMT_1 = 0x6B
    SMPLRT_DIV = 0x19
    CONFIG = 0x1A
    GYRO_CONFIG = 0x1B
    INT_ENABLE = 0x38
    ACCEL_X = 0x3B
    ACCEL_Y = 0x3D
    ACCEL_Z = 0x3F
    GYRO_X = 0x43
    GYRO_Y = 0x45
    GYRO_Z = 0x47

    bus = smbus.SMBus(1)
    device_address = 0x68  # MPU6050 device address

    def __init__(self):
        # write to sample rate register
        self.bus.write_byte_data(self.device_address, self.SMPLRT_DIV, 7)

        # Write to power management registerp
        self.bus.write_byte_data(self.device_address, self.PWR_MGMT_1, 1)

        # Write to Configuration register
        self.bus.write_byte_data(self.device_address, self.CONFIG, 0)

        # Write to Gyro configuration register
        self.bus.write_byte_data(self.device_address, self.GYRO_CONFIG, 24)

        # Write to interrupt enable register
        self. bus.write_byte_data(self.device_address, self.INT_ENABLE, 1)

    def read_raw_data(self, addr):
        # Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(self.device_address, addr)
        low = self.bus.read_byte_data(self.device_address, addr + 1)

        # concatenate higher and lower value
        value = ((high << 8) | low)

        # to get signed value from mpu6050
        if value > 32768:
            value = value - 65536
        return value