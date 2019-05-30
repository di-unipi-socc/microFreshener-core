from abc import ABC, abstractmethod
from ..model import MicroToscaModel 
 
class Importer(ABC):
 
    @abstractmethod
    def Import(self, path:str)->MicroToscaModel:
        pass