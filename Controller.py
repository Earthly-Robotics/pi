from Network.NetworkController import *
from ComponentControllers.VisionController import VisionController
import cv2 as cv

def main():
    # server = NetworkController()
    # server.setup_server()

    vision_controller = VisionController()

    while True:
        vision_controller.get_camera_feed()
        cv.waitKey(1)

main()

