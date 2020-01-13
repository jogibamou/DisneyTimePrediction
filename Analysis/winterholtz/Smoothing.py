from DatasetAPI.thundermountain_wait_dataset import Dataset
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

max_seasons = list(range(24))

class winterholtz(object):
    def __init__(self, data, excluded_hours = list(range(19,24)) + list(range(0,9))):
        endog = data.get_data_raw()
        endog = data.prune_data_hours(endog, excluded_hours)
        endog = data.get_data_averaged_hour(endog)
        endog = data.get_data_by_day(endog)
        endog = data.transform_from_lists_to_list(endog)
        self.__full_time_series = data.get_time_series(endog)
        self.__number_of_seasons = len(max_seasons) - len(excluded_hours)
        for i in self.__full_time_series:
            if i < 0:
                print(i)

    def get_length(self):
        return len(self.__full_time_series)

    def get_season(self):
        return self.__number_of_seasons

    def get_data(self):
        return self.__full_time_series

    def get_diff_set(self, predict, ground):
        return np.abs(np.subtract(predict, ground))

    def get_statistics(self, predict, ground):
        diff_set = self.get_diff_set(predict, ground)
        return {"Average" : np.average(diff_set), "Standard deviation" : np.std(diff_set), "Maximum" : np.max(diff_set),
        "Minimum" : np.min(diff_set), "Predictions" : predict, "Ground Truth" : ground}

    def get_smooth_over_interval(self, start, stop):
        return ExponentialSmoothing(self.__full_time_series[start:stop], "add", True, "add", self.__number_of_seasons).fit()

    def test_smooth(self, smooth, start, stop):
        return self.get_statistics(smooth.predict(start, stop -1), self.__full_time_series[start:stop])
        # return np.average(np.abs(np.subtract(smooth.predict(start, stop - 1), self.__full_time_series[start:stop])))

    def smooth_then_test(self, start, smoothsize, testsize):
        smoothindex = smoothsize + start
        testindex = smoothindex + testsize
        return self.test_smooth(self.get_smooth_over_interval(start, smoothindex), smoothindex, testindex)

    def smooth_then_test_over_range(self, start, stop, smoothsize, testsize):
        smooths = []
        for test_set in range(start, stop - smoothsize - testsize, smoothsize + testsize):
            smooths.append(self.smooth_then_test(test_set,  smoothsize, testsize)["Average"])
        fakeground = np.zeros(len(smooths))
        return self.get_statistics(smooths, fakeground)

    def smooth_then_test_over_range_verbose(self, start, stop, smoothsize, testsize):
        smooths = []
        for test_set in range(start, stop - smoothsize - testsize, smoothsize + testsize):
            smooths.append(self.smooth_then_test(test_set,  smoothsize, testsize))
            print(f"{test_set} / {stop}")
        return smooths




