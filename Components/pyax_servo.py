import serial
import time
from pyax12.connection import Connection


def main():
    """
    This is an *endless turn mode* demo.
    If both values for the *CW angle limit* and *CCW angle limit* are set to 0,
    an *endless turn mode* can be implemented by setting the *goal speed*.
    This feature can be used for implementing a continuously rotating wheel.
    """

    # Connect to the serial port
    serial_connection = Connection(pport="/dev/ttyAMA0",
                                   baudrate=1000000,
                                   rpi_gpio=True)

    dynamixel_id = 1

    # Set the "wheel mode"
    serial_connection.set_cw_angle_limit(dynamixel_id, 0, degrees=False)
    serial_connection.set_ccw_angle_limit(dynamixel_id, 0, degrees=False)

    # Activate the actuator (speed=512)
    serial_connection.set_speed(dynamixel_id, 512)

    # Lets the actuator turn 5 seconds
    time.sleep(5)

    # Stop the actuator (speed=0)
    serial_connection.set_speed(dynamixel_id, 0)

    # Leave the "wheel mode"
    serial_connection.set_ccw_angle_limit(dynamixel_id, 1023, degrees=False)

    # Go to the initial position (0 degree)
    serial_connection.goto(dynamixel_id, 0, speed=512, degrees=True)

    # Close the serial connection
    serial_connection.close()


if __name__ == '__main__':
    main()