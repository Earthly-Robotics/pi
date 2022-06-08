from Network.NetworkController import *
from ComponentControllers.VisionController import VisionController
from Components.Camera import Camera
from Components.CameraFeed import CameraFeed
import cv2 as cv

def main():
    vision_controller = VisionController()
    camerafeed = CameraFeed(vision_controller.cam, vision_controller)
    server = NetworkController(camerafeed)
    server.setup_server()

main()
