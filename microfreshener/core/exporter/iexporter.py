from abc import ABC, abstractmethod
from ..model import MicroToscaModel 
 
class Exporter(ABC):
 
    @abstractmethod
    def Export(self, model:MicroToscaModel)->str:
        pass
