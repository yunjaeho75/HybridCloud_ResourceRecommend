from abc import *

class AbstractHelper(metaclass=ABCMeta):
    @abstractmethod
    def names(self) -> str:
        pass

    @abstractmethod
    def summary(self):
        pass
    
    @abstractmethod
    def create(self, parameter):
        pass

    @abstractmethod
    def summary(self):
        pass

    @abstractmethod
    def summary_str(self):
        pass

    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def load(self, path):
        pass

    @abstractmethod
    def save(self, path):
        pass

    @abstractmethod
    def evaluate(self, data):
        pass

    @abstractmethod
    def predict(self, data):
        pass
        
        