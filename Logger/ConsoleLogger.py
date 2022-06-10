from Logger.ILogger import ILogger


class ConsoleLogger(ILogger):

    def log(self, string):
        print(string)
