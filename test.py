from realsense_api.post_processing.decimation import Decimation
from realsense_api.post_processing.spatial import Spatial

a=Decimation()
print(a)
print(a.magnitude)

a.increment()
print(a.magnitude)

a.increment()
print(a.magnitude)

a.increment()
print(a.magnitude)

a.increment()
print(a.magnitude)

a.increment()
print(a.magnitude)

a.increment()
print(a.magnitude)

a.increment()
print(a.magnitude)

a.increment()
print(a.magnitude)

b=Spatial()
print(b)
b.increment(value='smooth alpha')
print(b)