from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class FilterOptions(ABC):

    @abstractmethod
    def increment(self):
        pass