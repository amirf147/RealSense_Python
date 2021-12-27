from typing import TypedDict
from dataclasses import dataclass
from enum import Enum, auto

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

class Options(TypedDict):
    option: OptionType
    properties : OptionValues