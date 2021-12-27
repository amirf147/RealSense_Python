# https://dev.intelrealsense.com/docs/post-processing-filters
from dataclasses import asdict, dataclass, field

from option import OptionValues, OptionType, Options
from filter import FilterOptions

class SpatialOptions(FilterOptions):
    options: Options = {
        OptionType.MAGNITUDE: OptionValues(
            option_value=2,
            option_value_increment=1,
            option_min_value=0,
            option_max_value=5
        ),    
        OptionType.SMOOTH_ALPHA : OptionValues(
            option_value=0.5,
            option_value_increment=0.25,
            option_min_value=0.0,
            option_max_value=1.0
        ),
        OptionType.SMOOTH_DELTA: OptionValues(
            option_value=2,
            option_value_increment=1,
            option_min_value=0,
            option_max_value=5
        ),
        OptionType.HOLE_FILLING: OptionValues(
            option_value=0,
            option_value_increment=1,
            option_min_value=0,
            option_max_value=5
        )
    }

    def increment(self, option: OptionValues):
        option.option_value += option.option_value_increment
        if option.option_value > option.option_max_value:
            option.option_value = option.option_min_value


spatial_filter = SpatialOptions()
# spatial_options = asdict(spatial_filter.options)
spatial_filter_hole_filling = spatial_filter.options[OptionType.HOLE_FILLING]
for i in range(20):
    print(spatial_filter_hole_filling.option_value)        
    spatial_filter.increment(spatial_filter_hole_filling)

print(type(spatial_filter))
# for i,v in spatial_options.items():
#     print(i,v)

# =a.hole_filling
# print(o.option_value)
# for i in range(7):
#     a.increment(o)
# for i in spatial_filter.options:
#     print(i)
  