import asyncio, time
from ComponentControllers.VisionController import VisionController
from ComponentControllers.ArduinoController import ArduinoController
from Components.GyroAccelerometer import GyroAccelerometer

# vision_controller = VisionController()


async def main():
    # arduino_controller = arduino_setup()
    # vision_controller.track_blue_cube()
    # arduino_controller.close()


def arduino_setup():
    controller = ArduinoController()
    controller.connect()
    asyncio.create_task(controller.read_message())
    return controller


asyncio.run(main())
