from abc import ABC, abstractmethod

class Strategy(ABC):

    @abstractmethod
    def resolver(estado_inicial):
        pass
