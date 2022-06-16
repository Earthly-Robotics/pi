import serial, time, asyncio
from Logger.ConsoleLogger import ConsoleLogger


class ArduinoController:
    logger = ConsoleLogger()
    arduino = None
    n_reads = 4
    delay = 20
    baudrate = 9600
    port = "/dev/ttyUSB0"

    def connect(self) -> None:
        """
        Creates a serial connection to the arduino
        """
        arduino = serial.Serial(self.port, self.baudrate, timeout=1)
        time.sleep(0.1)
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            self.arduino = arduino

    def send_message(self, msg) -> None:
        """
        Sends a message to the connected arduino

        :param msg: The message that will be sent to the arduino
        :type msg: str
        """
        if self.arduino is not None:
            try:
                self.arduino.write(msg.encode())
                self.arduino.flush()
            except Exception as e:
                print("Could not write to arduino:\n{0}".format(e))

    async def read_message(self) -> None:
        """
        Continuously write received messages from the arduino to log.
        """
        if self.arduino is not None:
            while self.arduino.isOpen():
                msg = b""
                for _ in range(self.n_reads):
                    msg += self.arduino.read_until()
                if msg != b"":
                    self.logger.log(msg.decode())
                self.arduino.reset_input_buffer()
                await asyncio.sleep(0.8 * self.n_reads * self.delay / 1000)
        else:
            print("Arduino is None... Try calling connect()")
            return

    def close(self) -> None:
        """
        Closes the serial connection to the arduino
        """
        self.arduino.close()
