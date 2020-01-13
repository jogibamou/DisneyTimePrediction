from DatasetAPI.thundermountain_wait_dataset import Dataset
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

data = Dataset("public", "soarin_data", 100000000)

endog = data.get_data_raw()
endog = data.prune_data_hours(endog)
endog = data.get_data_averaged_hour(endog)
endog = data.get_data_by_day(endog)

maxlen = len(endog[0])
for end in endog:
    if len(end) > maxlen:
        maxlen = len(end)
print("Max length " + str(maxlen))


newendog = []
for end in endog:
    if maxlen == len(end):
        newendog.append(end)

print("Length of endog " + str(len(endog)))
print("Length of new endog " + str(len(newendog)))
endog = data.transform_from_lists_to_list(newendog)
endog = data.get_time_series(endog)
print(f"Length of time series {len(endog)}")

seasonal_period = 11

smooth = ExponentialSmoothing(endog[2000:3015], "add", True, "add", seasonal_period).fit()

val = smooth.predict(3000, 3055)

val = np.array(val)

val=np.subtract(val, endog[3000:3056])

val =np.abs(val)

print(f"Average {np.average(val)}")
print(f"Standard deviation {np.std(val)}")
print(f"Max {np.max(val)}")
print(f"Min {np.min(val)}")

# count = 0
# print(endog[990:1030])
# for y_pre,y_act in zip(smooth.predict(start=4000,end=4020), endog[4000:4021]):
#     count += 1
#     if abs(y_pre-y_act) > 30:
#         print(str(count) + ":")
#         print(y_pre)
#         print(y_act)
#         print('-----')