import asyncio
import platform
import threading
import RPi.GPIO as GPIO

from Logger.ConsoleLogger import ConsoleLogger
from Logger.FileLogger import FileLogger
from Network.NetworkController import NetworkController
from ComponentControllers.ArduinoController import ArduinoController

from Components.AutoSeedPlant import AutoSeedPlant


async def main(arduino_controller):
    thread = None
    try:
        server = NetworkController(arduino_controller)
        thread = threading.Thread(target=server.setup_server, daemon=True)
        thread.start()
    except KeyboardInterrupt:
        pass
    finally:
        if thread is not None:
            thread.join()
    #auto_seed_plant = AutoSeedPlant()
    #auto_seed_plant.plant_seeds(2, 2, 30, 30)


def arduino_setup():
    controller = ArduinoController()
    controller.connect()
    # asyncio.create_task(controller.read_message())
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
        arduino_controller = arduino_setup()
        asyncio.run(main(arduino_controller))
    except KeyboardInterrupt:
        logger.log("Keyboard Interrupt!")
    except Exception as e:
        logger.log("Something went wrong in MAIN: {0}".format(e))
    finally:
        arduino_controller.close()
        GPIO.cleanup()
