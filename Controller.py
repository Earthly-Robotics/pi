from ComponentControllers.ArduinoController import ArduinoController
from Network.NetworkController import *

async def main():
    try:
        server = NetworkController()
        thread = threading.Thread(target=server.setup_server, daemon=True)
        thread.start()
    except KeyboardInterrupt:
        pass
    finally:
        if thread is not None:
            thread.join()


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
