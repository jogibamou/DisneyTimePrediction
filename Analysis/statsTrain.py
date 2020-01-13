from DatasetAPI.thundermountain_wait_dataset import Dataset
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

data = Dataset("public", "filtered_thundermountain_weather2", 5000)

endog = data.get_data_raw()
endog = data.prune_data_hours(endog)
endog = data.get_time_series(endog)
print(len(endog))
seasonal_period = 12

smooth = ExponentialSmoothing(endog[0:2000], "add", True, "add", seasonal_period).fit()

val = smooth.predict(start =2000,end= 2400)

val = np.array(val)

val=np.subtract(val, endog[2000:2401])

val =np.abs(val)

print(np.average(val))
print(np.std(val))
print(np.max(val))
print(np.min(val))


endog1 = endog[0:1000]
endog2 = endog[1400:2400]
print(np.average(np.abs(np.subtract(endog1,endog2))))


for y_pre,y_act in zip(smooth.predict(start=2000,end=2400), endog[2000:2401]):
    if abs(y_pre-y_act) > 30:
        print(y_pre)
        print(y_act)
        print('-----')