import Singleton
from Logger.ILogger import ILogger
from datetime import datetime


class FileLogger(ILogger, metaclass=Singleton):

    def log(self, string):
        dt = datetime.now()
        hour = dt.hour
        date = dt.date()
        minutes = dt.minute
        with open("./Logs/{}-{}.log".format(date, hour), "a") as f:
            f.write(("\n" + "{}: " + string).format(minutes))