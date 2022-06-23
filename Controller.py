import asyncio
import threading
import platform
import traceback

import RPi.GPIO as GPIO
from Network.NetworkController import NetworkController
from ComponentControllers.ArduinoController import ArduinoController
from Logger.ConsoleLogger import ConsoleLogger
from Logger.FileLogger import FileLogger


async def main():
    arduino_controller = arduino_setup()
    # arduino_controller = None
    # arduino_controller.close()
    server = None
    thread = None
    try:
        server = NetworkController(arduino_controller)
        # server = NetworkController()
        thread = threading.Thread(target=server.setup_server, daemon=True)
        thread.start()
    except KeyboardInterrupt:
        pass
    finally:
        if server is not None:
            server.stop_server()
        if thread is not None:
            thread.join()
            arduino_controller.close()


def arduino_setup():
    controller = ArduinoController()
    controller.connect()
    asyncio.create_task(controller.read_message())
    return controller


if __name__ == "__main__":
    match platform.system():
        case "Windows":
            logger = ConsoleLogger()
        case "Linux":
            logger = ConsoleLogger()
        case _:
            logger = FileLogger()
            logger.log("System not recognized")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.log("Keyboard Interrupt!")
    except Exception as e:
        logger.log("Something went wrong in MAIN: {0}".format(e))
    finally:
        GPIO.cleanup()
