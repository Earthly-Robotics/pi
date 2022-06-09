from Network.NetworkController import *
from ComponentControllers.VisionController import VisionController
from ComponentControllers.WheelsController import WheelsController
from Components.CameraFeed import CameraFeed
import cv2 as cv

def main():
    vision_controller = VisionController()
    camera_feed = CameraFeed(vision_controller.cam,vision_controller)
    wheels_controller = WheelsController()
    server = NetworkController(camera_feed, wheels_controller)
    server.setup_server()

main()
