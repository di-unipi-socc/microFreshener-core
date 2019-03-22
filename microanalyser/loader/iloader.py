from abc import ABC, abstractmethod
from ..model.template import MicroModel 
 
class Loader(ABC):
 
    @abstractmethod
    def load(self, path:str)->MicroModel:
        pass