from typing import TypedDict
from dataclasses import dataclass
from enum import Enum, auto
from abc import ABC, abstractmethod

class OptionType(Enum):
    MAGNITUDE = auto()
    SMOOTH_ALPHA = auto()
    SMOOTH_DELTA = auto()
    HOLE_FILLING = auto()
    PERSISTENCY_INDEX = auto()

@dataclass
class OptionValues():
    option_value: int
    option_value_increment: int
    option_min_value: int
    option_max_value: int

# class OptionDict(TypedDict):
#     option: OptionType
#     properties : OptionValues

class FilterOptions(ABC):    
    @abstractmethod
    def increment(self) -> None:
        pass
