from abc import ABC, abstractmethod
from ..model.template import MicroModel 
 
class Transformer(ABC):
 
    @abstractmethod
    def transform(self, model:MicroModel)->str:
        pass
