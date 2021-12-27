# https://dev.intelrealsense.com/docs/post-processing-filters
from dataclasses import asdict, dataclass

from option import Option, OptionType
from filter import FilterOptions

@dataclass
class SpatialOptions(FilterOptions):
    magnitude: Option = Option(
        option_type=OptionType.MAGNITUDE,
        option_value=2,
        option_value_increment=1,
        option_min_value=0,
        option_max_value=5
    )
    smooth_alpha: Option = Option(
        option_type=OptionType.SMOOTH_ALPHA,
        option_value=0.5,
        option_value_increment=0.25,
        option_min_value=0.0,
        option_max_value=1.0
    )
    smooth_delta: Option = Option(
        option_type=OptionType.SMOOTH_DELTA,
        option_value=2,
        option_value_increment=1,
        option_min_value=0,
        option_max_value=5
    )
    hole_filling: Option = Option(
        option_type=OptionType.HOLE_FILLING,
        option_value=0,
        option_value_increment=1,
        option_min_value=0,
        option_max_value=5
    )  
    
    def increment(self, option: Option):
        option.option_value += option.option_value_increment
        if option.option_value > option.option_max_value:
            option.option_value = option.option_min_value

@dataclass
class Spatial():
    options: SpatialOptions = SpatialOptions()

    # def asdict(self):
    #     return {}

spatial_filter = Spatial()
# spatial_options = asdict(spatial_filter.options)
# # print(spatial)

# for i,v in spatial_options.items():
#     print(i,v)

# =a.hole_filling
# print(o.option_value)
# for i in range(7):
#     a.increment(o)
# for i in spatial_filter.options:
#     print(i)
  