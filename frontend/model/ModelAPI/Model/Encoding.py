import numpy as np

class Encoding(object):
    def __init__(self):
        # Periods 
        self.day_period_mapping = {}
        self.season_period_mapping = {}
        self.wait_time_mapping = {}
        self.precipitation_categories = {} # Use tuples to represent real ranges
        self.temp_categories = []
        self.__last_wait_time = [0]
        ### Set up hour/period mapping ###
        # periods of the day as hours of a 24 hour day
        morning = range(8, 11)
        midday = range(11, 13)
        afternoon = range(13, 16)
        evening = range(16, 20)
        night = range(20, 24)
        latenight = range(0, 8)
        self.max_hour_in_day = len([morning, midday, afternoon, evening, night, latenight])
        
        spring = range(2,5)
        summer = range(5,8)
        fall = range(8,11)
        winter = [11, 0, 1]
        self.max_season_in_year = len([spring, summer, fall, winter])

        wt_0 = [0]
        wt_5_10 = [5,10]
        wt_15_20 = [15, 20]
        wt_25_30 = [25, 30]
        wt_35_40 = [35,40]
        wt_45_50 = [45, 50]
        wt_55_60 = [55, 60]
        wt_65_70 = [65, 70]
        wt_75_80 = [75, 80]
        wt_90_120 = range(85, 120)
        wt_120_400 = range(120, 401)
        self.max_waittimes_in_set = len(list([wt_0, wt_5_10, wt_15_20, wt_25_30, wt_35_40, wt_45_50, wt_55_60, wt_65_70, wt_75_80, wt_90_120, wt_120_400]))


        for hour in range(24):
            if hour in morning:    self.day_period_mapping[hour] = 0
            if hour in midday:     self.day_period_mapping[hour] = 1
            if hour in afternoon:  self.day_period_mapping[hour] = 2
            if hour in evening:    self.day_period_mapping[hour] = 3
            if hour in night:      self.day_period_mapping[hour] = 4
            if hour in latenight:  self.day_period_mapping[hour] = 5

        for month in range(12):
            if month in spring: self.season_period_mapping[month] = 0
            if month in summer: self.season_period_mapping[month] = 1
            if month in fall: self.season_period_mapping[month] = 2
            if month in winter: self.season_period_mapping[month] = 3

        for time in range(0, 405, 5):
            if time in wt_0: self.wait_time_mapping[time] = 0
            if time in wt_5_10: self.wait_time_mapping[time] = 1
            if time in wt_15_20: self.wait_time_mapping[time] = 2
            if time in wt_25_30: self.wait_time_mapping[time] = 3
            if time in wt_35_40: self.wait_time_mapping[time] = 4
            if time in wt_45_50: self.wait_time_mapping[time] = 5
            if time in wt_55_60: self.wait_time_mapping[time] = 6
            if time in wt_65_70: self.wait_time_mapping[time] = 7
            if time in wt_75_80: self.wait_time_mapping[time] = 8
            if time in wt_90_120: self.wait_time_mapping[time] = 9
            if time in wt_120_400: self.wait_time_mapping[time] = 10

        # self.precipitation_categories[0] = (0, 0.0001)
        # self.precipitation_categories[1] = (0, 0.244)
        # self.precipitation_categories[2] = (0.244, 0.632)
        # self.precipitation_categories[3] = (0.632, 10000)

        # self.temp_categories[0] = (0,30)
        # self.temp_categories[1] = (30,40)
        # self.temp_categories[2] = (40,50)
        # self.temp_categories[3] = (50,60)
        # self.temp_categories[4] = (60,70)
        # self.temp_categories[5] = (70,80)
        # self.temp_categories[6] = (80,90)
        # self.temp_categories[7] = (90,100)
        # self.temp_categories[8] = (100,110)

        # Weather
        # Clear weather
        self.precipitation_categories["Clear"] = 0
        self.precipitation_categories["Clouds"] = 1
        self.precipitation_categories["Drizzle"] = 2
        self.precipitation_categories["Fog"] = 3
        self.precipitation_categories["Haze"] = 4
        self.precipitation_categories["heavy intensity rain"] = 5
        self.precipitation_categories["light intensity shower rain"] = 6
        self.precipitation_categories["light rain"] = 7
        self.precipitation_categories["Mist"] = 8
        self.precipitation_categories["moderate rain"] = 9
        self.precipitation_categories["proximity moderate rain"] = 10
        self.precipitation_categories["proximity shower rain"] = 11
        self.precipitation_categories["proximity thunderstorm"] = 12
        self.precipitation_categories["shower rain"] = 13
        self.precipitation_categories["Smoke"] = 14
        self.precipitation_categories["thunderstorm"] = 15
        self.precipitation_categories["thunderstorm with heavy rain"] = 16
        self.precipitation_categories["thunderstorm with light rain"] = 17
        self.precipitation_categories["thunderstorm with rain"] = 18
        self.precipitation_categories["very heavy rain"] = 19



        # Temperature
        self.temp_categories = [(x,y) for x,y in zip(range(265,310,5), range(270,315,5))]


    def encode_onehot_hour(self, hour):
        if(hour < 0 or hour > 24):
            print(hour)
            raise Exception(f"{hour} Not a real hour")
        encoded = self.encode_as_ith_element(int(hour), 24)
        return encoded
    
    def encode_onehot_month(self, month):
        num_months = 12
        if(month < 1 or month > num_months):
            raise Exception("Not a real month")
        month = int(month)
        encoded  = self.encode_as_ith_element(month-1, num_months)
        return encoded
    
    def encode_onehot_season(self, month):
        num_months = 12
        if(month < 1 or month > num_months):
            raise Exception("Not a real month")
        encoded = self.encode_as_ith_element(self.season_period_mapping[month - 1], self.max_season_in_year)
        return encoded

    def encode_onehot_wait_time(self, wait_time):
        if(wait_time < 0 or wait_time > 400):
           raise Exception("Not a valid wait time")
        encoded = self.encode_as_ith_element(self.wait_time_mapping[wait_time], self.max_waittimes_in_set)
        return self.wait_time_mapping[wait_time]

    def encode_onehot_dow(self, day):
        day_dim = 7
        if(day < 0 or day > 6):
            raise Exception("Not a valid day")
        day = int(day)
        encoded = self.encode_as_ith_element(day, day_dim)
        return encoded

    def encode_onehot_precipitation(self, precip):
        return self.encode_as_ith_element(self.precipitation_categories[precip], len(self.precipitation_categories.keys()))

    def encode_onehot_temp(self, temp):
        index = self.map_float_to_range(temp, self.temp_categories)
        return self.encode_as_ith_element(index, len(self.temp_categories))


    def binary_wait_time(self, wait_time):
        if(wait_time < 0 or wait_time > 400):
            raise Exception("Not a valid wait time")
        val = 1 if wait_time > 0 else 0
        return self.encode_as_ith_element(val, 2)

    def analog_wait_time(self, wait_time, avg_val, std_val, min_val, max_val):
        return [wait_time/max_val]
        # above = (max_val - avg_val) / (std_val)
        # below = (avg_val - min_val) / (std_val)
        # if(wait_time > avg_val):
        #     deviations = (wait_time - avg_val) / std_val
        #     return [1*(.5 + (deviations / (above * 2)))]
        # else:
        #     deviations = (avg_val - wait_time) / std_val
        #     return [1*(.5 - (deviations / (below * 2)))]

    def encode_last_wait_time(self, wait_time, max_val):
        tmp = self.__last_wait_time
        self.__last_wait_time = [wait_time/max_val]
        return tmp


    # Index starts at 0
    def encode_as_ith_element(self, index, dimensions):
        if(index > dimensions):
            raise Exception("One hot: index > dimensions")
        encoded_value = np.zeros(dimensions)
        encoded_value[index] = 1
        return encoded_value

    def map_float_to_range(self, i, ranges):
        count = 0
        for item in ranges:
            if(i >= item[0] and i < item[1]):
                return count
            else:
                count += 1
        raise Exception(f"Value {i} did not match any of the provided ranges")