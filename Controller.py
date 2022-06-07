from Network.NetworkController import *
from ComponentControllers.VisionController import VisionController
from ComponentControllers.WheelsController import WheelsController
from Components.CameraFeed import CameraFeed


def main():
    wheels_controller = WheelsController()
    server = NetworkController(wheels_controller)
    server.setup_server()


main()

