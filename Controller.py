import asyncio
import cv2 as cv
import threading

from ComponentControllers.VisionController import VisionController
from ComponentControllers.ArduinoController import ArduinoController
from Components.LoadCell import LoadCell
#from Components.GyroAccelerometer import GyroAccelerometer
from Network.NetworkController import *


async def main():
    # arduino_controller = arduino_setup()
    # arduino_controller.close()
    server = NetworkController()
    thread = threading.Thread(target=server.setup_server, daemon=True)
    thread.start()
    try:
        load_cell = LoadCell()
        while True:
            print(load_cell.measure_weight())
    except KeyboardInterrupt:
        print("Keyboard interrupt detected")


def arduino_setup():
    controller = ArduinoController()
    controller.connect()
    asyncio.create_task(controller.read_message())
    return controller


if __name__ == "__main__":
    asyncio.run(main())
