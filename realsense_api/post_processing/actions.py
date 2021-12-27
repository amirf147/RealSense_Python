from abc import ABC, abstractmethod

class Increment(ABC):
    @abstractmethod
    def increment(self, value, increment, max_value, min_value) -> None:
        value += increment
        if value > max_value:
            value = min_value