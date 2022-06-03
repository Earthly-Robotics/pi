from Network.NetworkController import *


def main():
    server = NetworkController()
    server.setup_server()


main()

from Command import Command
from WheelsController import WheelsController


class Controller:
    def on_input_receive(self):
        cmd = Command()
        cmd.joystick_position_x = 1011
        cmd.joystick_position_y = 1

        if cmd.joystick_position_x != 512 or cmd.joystick_position_y != 512:
            wheels_controller = WheelsController()
            wheels_controller.move_logic(cmd)


controller = Controller()

while True:
    controller.on_input_receive()
