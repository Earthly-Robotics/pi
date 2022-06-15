from Network.NetworkController import *
from ComponentControllers.VisionController import VisionController
from ComponentControllers.WheelsController import WheelsController
from Components.CameraFeed import CameraFeed
import asyncio
import cv2 as cv
import threading

#from ComponentControllers.VisionController import VisionController
#from ComponentControllers.ArduinoController import ArduinoController
#from Components.LoadCell import LoadCell
#from Components.GyroAccelerometer import GyroAccelerometer
from Network.NetworkController import *


async def main():
    # arduino_controller = arduino_setup()
    # arduino_controller.close()
    try:
        vision_controller = VisionController()
        camera_feed = CameraFeed(vision_controller.cam,vision_controller)
        wheels_controller = WheelsController()
        server = NetworkController(camera_feed, wheels_controller)
        thread = threading.Thread(target=server.setup_server, daemon=True)
        thread.start()
    except KeyboardInterrupt:
        pass
    finally:
        if thread is not None:
            thread.join()

def arduino_setup():
    controller = ArduinoController()
    controller.connect()
    asyncio.create_task(controller.read_message())
    return controller


if __name__ == "__main__":
    asyncio.run(main())
