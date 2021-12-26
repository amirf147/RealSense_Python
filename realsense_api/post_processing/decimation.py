# https://dev.intelrealsense.com/docs/post-processing-filters
from dataclasses import dataclass
from realsense_api.post_processing.filter import Filter

@dataclass
class Decimation(Filter):
    magnitude:           int = 2
    magnitude_increment: int = 1
    max_magnitude:       int = 8
    min_magnitude:       int = 1

    # def increment(self):
    #     self.magnitude += self.magnitude_increment
    #     if self.magnitude > self.max_magnitude:
    #         self.magnitude = self.min_magnitude # Turn off filter
    
    # Since it is not possible to add instance variables into a class
    # method as default parameters, a common work-around was applied 
    def increment(self, 
                  value=None,
                  increment=None,
                  max_value=None,
                  min_value=None) -> None:
        if value is None:
            value = self.magnitude
        if increment is None:
            increment = self.magnitude_increment
        if max_value is None:
            max_value = self.max_magnitude
        if min_value is None:
            min_value = self.min_magnitude
        value += increment
        if value > max_value:
            value = min_value
        self.magnitude = value