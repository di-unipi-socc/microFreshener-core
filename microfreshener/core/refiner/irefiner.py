from abc import ABC, abstractmethod
from ..model import MicroToscaModel 


class Refiner(ABC):
 
    @abstractmethod
    def Refine(self, microtosca:MicroToscaModel)->MicroToscaModel:
        pass