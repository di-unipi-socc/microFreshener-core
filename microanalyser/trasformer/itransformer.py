from abc import ABC, abstractmethod
from ..model.template import MicroModel 
 
class Trasnformer(ABC):
    @abstractmethod
    def load(self, model:MicroModel)->file:str
        pass
