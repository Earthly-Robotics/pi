from Network.NetworkController import *
from ComponentControllers.VisionController import VisionController
from ComponentControllers.WheelsController import WheelsController
from Components.CameraFeed import CameraFeed


def main():
    # vision_controller = VisionController()
    # camera_feed = CameraFeed(vision_controller.cam)
    wheels_controller = WheelsController()
    # server = NetworkController(wheels_controller, vision_controller, camera_feed)
    server = NetworkController(wheels_controller)
    server.setup_server()

    # vision_controller = VisionController()
    #
    # while True:
    #     vision_controller.get_camera_feed()
    #     cv.waitKey(1)


main()

