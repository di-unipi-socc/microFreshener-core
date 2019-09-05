from abc import ABC, abstractmethod
from ..model import MicroToscaModel


class IRefiner(ABC):

    @abstractmethod
    def Refine(self, microtosca: MicroToscaModel) -> MicroToscaModel:
        pass
