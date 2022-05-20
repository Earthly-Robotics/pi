from Logger.ILogger import ILogger
from datetime import datetime


class FileLogger(ILogger):

    def log(self, string):
        dt = datetime.now()
        hour = dt.hour
        date = dt.date()
        with open("./Logs/{}-{}.log".format(date, hour), "a") as f:
            f.write("\n" + string)



