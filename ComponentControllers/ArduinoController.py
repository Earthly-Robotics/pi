import serial, time, asyncio

class ArduinoController:
    arduino = None
    n_reads = 4
    delay = 20

    def connect(self):
        arduino = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
        time.sleep(0.1)
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            self.arduino = arduino

    def send_message(self, msg):
        if self.arduino is not None:
            try:
                self.arduino.write(msg.encode())
                self.arduino.flush()
            except Exception as e:
                print("Could not write to arduino:\n{0}".format(e))

    async def read_message(self):
        if self.arduino is not None:
            while self.arduino.isOpen():
                msg = b""
                for _ in range(self.n_reads):
                    msg += self.arduino.read_until()
                if msg != b"":
                    print(msg.decode())
                self.arduino.reset_input_buffer()
                await asyncio.sleep(0.8 * self.n_reads * self.delay / 1000)
        else:
            print("Arduino is None... Try calling connect()")
            return

    def close(self):
        self.arduino.close()
