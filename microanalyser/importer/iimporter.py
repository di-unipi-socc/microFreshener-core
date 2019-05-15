from abc import ABC, abstractmethod
from ..model import MicroModel 
 
class Importer(ABC):
 
    @abstractmethod
    def Import(self, path:str)->MicroModel:
        pass