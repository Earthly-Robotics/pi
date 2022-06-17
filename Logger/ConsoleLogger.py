import Singleton
from Logger.ILogger import ILogger


class ConsoleLogger(ILogger, metaclass=Singleton):

    def log(self, string):
        print(string)
