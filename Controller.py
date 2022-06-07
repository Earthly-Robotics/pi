from Network.NetworkController import *
from ComponentControllers.VisionController import VisionController
import cv2 as cv
from ComponentControllers.WheelsController import WheelsController

def main():
    vision_controller = VisionController()
    server = NetworkController(vision_controller)
    wheels_controller = WheelsController()
    server = NetworkController(wheels_controller)
    server.setup_server()

    # vision_controller = VisionController()
    #
    # while True:
    #     vision_controller.get_camera_feed()
    #     cv.waitKey(1)

main()

