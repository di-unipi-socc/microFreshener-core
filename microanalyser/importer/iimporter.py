from abc import ABC, abstractmethod
from ..model.template import MicroModel 
 
class Importer(ABC):
 
    @abstractmethod
    def Import(self, path:str)->MicroModel:
        pass