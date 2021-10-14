from abc import *

class AbstractHelper(metaclass=ABCMeta):
    @abstractmethod
    def names(self):
        pass

    @abstractmethod
    def window_parameter(self):
        pass
    
    @abstractmethod
    def load_data(self, ws):
        pass