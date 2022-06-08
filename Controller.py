import asyncio

import cv2 as cv

from ComponentControllers.VisionController import VisionController
from ComponentControllers.ArduinoController import ArduinoController
#from Components.GyroAccelerometer import GyroAccelerometer

# vision_controller = VisionController()


async def main():
    arduino_controller = arduino_setup()
    arduino_controller.close()


def arduino_setup():
    controller = ArduinoController()
    controller.connect()
    asyncio.create_task(controller.read_message())
    return controller

# while True:
#     vision_controller.track_blue_cube()
#     cv.waitKey(1)
asyncio.run(main())
