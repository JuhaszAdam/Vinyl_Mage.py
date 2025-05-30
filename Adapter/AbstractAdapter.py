from abc import ABC, abstractmethod
from typing import Type

from Model.Vinyl import Vinyl


class AbstractAdapter(ABC):

    @abstractmethod
    def adapt(self, vinyl_data:dict) -> Type[Vinyl]:
        pass
