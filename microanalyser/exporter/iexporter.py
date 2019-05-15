from abc import ABC, abstractmethod
from ..model import MicroModel 
 
class Exporter(ABC):
 
    @abstractmethod
    def Export(self, model:MicroModel)->str:
        pass
