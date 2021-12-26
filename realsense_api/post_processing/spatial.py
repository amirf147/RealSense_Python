# https://dev.intelrealsense.com/docs/post-processing-filters
from dataclasses import dataclass

@dataclass
class Spatial:
    magnitude:              int = 2
    magnitude_increment:    int = 1
    max_magnitude:          int = 5
    min_magnitude:          int = 0

    smooth_alpha:           float = 0.5
    smooth_alpha_increment: float = 0.25
    max_smooth_alpha:       float = 1.0
    min_smooth_alpha:       float = 0.0

    smooth_delta:           int = 20
    smooth_delta_increment: int = 1
    max_smooth_delta:       int = 50
    min_smooth_delta:       int = 0

    hole_filling:           int = 0
    hole_filling_increment: int = 1
    max_hole_filling:       int = 5
    min_hole_filling:       int = 0
    
    
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
            
        elif value == 'smooth alpha':
            value = self.smooth_alpha
            if increment is None:
                increment = self.smooth_alpha_increment
            if max_value is None:
                max_value = self.max_smooth_alpha
            if min_value is None:
                min_value = self.min_smooth_delta
            value += increment
            if value > max_value:
                value = min_value
            self.smooth_alpha = value

        elif value == 'smooth delta':
            value = self.smooth_delta
            if increment is None:
                increment = self.smooth_delta_increment
            if max_value is None:
                max_value = self.max_smooth_delta
            if min_value is None:
                min_value = self.min_smooth_delta
            value += increment
            if value > max_value:
                value = min_value
            self.smooth_delta = value

        elif value == 'hole filling':
            value = self.hole_filling
            if increment is None:
                increment = self.hole_filling_increment
            if max_value is None:
                max_value = self.max_hole_filling
            if min_value is None:
                min_value = self.min_hole_filling
            value += increment
            if value > max_value:
                value = min_value
            self.hole_filling = value