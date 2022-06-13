import time

import RPi.GPIO as GPIO
from Network.NetworkController import *
import threading
# from ComponentControllers.VisionController import VisionController
from ComponentControllers.WheelsController import WheelsController


def main():
    # vision_controller = VisionController()
    # camera_feed = CameraFeed(vision_controller.cam)
    try:
        wheels_controller = WheelsController()
        # server = NetworkController(wheels_controller, vision_controller, camera_feed)
        server = NetworkController(wheels_controller)
        server.setup_server()
        # server = NetworkController()
        # thread = threading.Thread(target=server.setup_server, daemon=True)
        # thread.start()
        # time.sleep(100)
        # print("done with main")

        # vision_controller = VisionController()
        #
        # while True:
        #     vision_controller.get_camera_feed()
        #     cv.waitKey(1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


main()

