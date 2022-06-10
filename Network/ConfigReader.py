import os
import platform
from configparser import ConfigParser
from Logger.ConsoleLogger import ConsoleLogger
from Logger.FileLogger import FileLogger


def config(section='PC'):
    """
    Returns an object containing the properties and values needed to connect to the corresponding database.

    :param section: Is either "staging" or "final". Defines the section of the config file in database.ini
    If not defined defaults to "staging".
    """
    match platform.system():
        case "Windows":
            logger = ConsoleLogger()
        case "Linux":
            logger = FileLogger()
        case _:
            logger = FileLogger()
            logger.log("System not recognized")

    while section not in ["PC", "Pi"]:
        logger.log(f'\033[1;31mWrong dbType: {section}\nIt should be either "staging" or "final"\033[1;37m')
        return

    parser = ConfigParser()
    cwd = os.getcwd()
    if cwd[-1] == 'o':
        parser.read('../Config.ini')
    else:
        parser.read('Config.ini')

    values = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            values[param[0]] = param[1]
    else:
        logger.log(str(Exception("Section {0} not found in database.ini".format(section))))
    return values
