from DatasetAPI.thundermountain_wait_dataset import Dataset 
from winterholtz.Smoothing import winterholtz
data = Dataset("public", "soarin_data", 10000000)
import numpy as np

winter = winterholtz(data)


# val1 = winter.test_smooth(smooth, 51, 65)["Average"]
# print(f"First smooth {val1}")

# val2 = winter.smooth_then_test(0, 24, 12)["Average"]

# print(f"Second smooth {val2}")

val3 = winter.smooth_then_test_over_range_verbose(0, 10000, winter.get_season() * 4,winter.get_season())

new_val3 = []
for item in val3:
    if item["Average"] > 0 and item["Average"] < 400:
        new_val3.append(item["Average"])

print(np.average(new_val3))
print(len(val3))
print(len(new_val3))


# print(f"Third smooth average {avg} {std} {best} {worst}")

#val3 = winter.smooth_then_test_over_range_verbose(0, 1000, winter.get_season() * 2,winter.get_season())

# worst_index = 0
# index = 0
# for item in val3:
#     if(val3[worst_index]["Average"] < item["Average"]):
#         worst_index = index
#     index += 1

# print(index)
# print(val3[worst_index])
# print(winter.get_data()[0:1000])
