from abc import ABC, abstractmethod
from ..model.template import MicroModel 
 
class Exporter(ABC):
 
    @abstractmethod
    def Export(self, model:MicroModel)->str:
        pass
