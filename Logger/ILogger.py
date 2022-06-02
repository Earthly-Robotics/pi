from abc import ABC, abstractmethod


class ILogger(ABC):

    @abstractmethod
    def log(self, string):
        pass
