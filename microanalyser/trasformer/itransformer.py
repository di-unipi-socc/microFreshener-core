from abc import ABC, abstractmethod
from ..model.template import MicroModel 
 
class Trasnformer(ABC):
 
    @abstractmethod
    def transform(self, model:MicroModel)->file:str
        pass
