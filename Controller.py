import cv2 as cv
from ComponentControllers.VisionController import VisionController

vision_controller = VisionController()

while True:
    vision_controller.track_blue_cube()
    cv.waitKey(1)
