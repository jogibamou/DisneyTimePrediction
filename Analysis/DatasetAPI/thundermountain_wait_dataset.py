from DatasetAPI import Datasets
from enum import Enum
import numpy as np
from DatasetAPI.encoding import Encoding
import random

TIMESTAMP = 0
WAITTIME = 1
MONTH = 2
DOW= 3
HOUR = 4
TEMP = 5
TEMP_MIN = 6
TEMP_MAX = 7
PRESSURE = 8
HUMIDITY = 9
WIND_SPEED = 10
WEATHER_CAT = 11

def round_to_nearest_five( val):
  new_val = val // 5 * 5
  new_val_mod = val % 5
  if new_val_mod > 5 // 2:
    new_val += 5
  return new_val

class Dataset:
  def __init__(self, dataset_dict, dataset_limit, train_cutoff = .8, val_cutoff = .9):
    self.__encode = Encoding()
    self.__accessor = Datasets.DataAccessor()
    self.__raw_data = self.__accessor.get(dataset_dict["schema"], dataset_dict["material"], limit = dataset_limit)
    self.__average = dataset_dict["avg"]
    self.__standard_deviation = dataset_dict["std"]
    self.__max_val = dataset_dict["max"]
    self.__min_val = dataset_dict["min"]
    self.__train_cutoff = train_cutoff
    self.__val_cutoff = val_cutoff

  def univariate_data(self, x_data, y_data, start_index, end_index, history_size, target_size):
    data = []
    labels = []
    x_data = np.array(x_data)
    y_data = np.array(y_data)
    start_index = start_index + history_size
    if end_index is None:
      end_index = len(x_data) - target_size

    for i in range(start_index, end_index):
      indices = range(i-history_size, i)
      # Reshape data from (history_size,) to (history_size, 1)
      data.append(np.reshape(x_data[indices], (history_size, len(x_data[0]))))
      labels.append(y_data[i+target_size])
    return np.array(data), np.array(labels)

  def get_data_encoded(self, data):
    x = []
    y = []

    for wait in data:
        month = self.__encode.encode_onehot_month(wait[MONTH])
        hour = self.__encode.encode_onehot_hour(wait[HOUR])
        day = self.__encode.encode_onehot_dow(wait[DOW])
        temp = self.__encode.encode_onehot_temp(wait[TEMP])
        precip = self.__encode.encode_onehot_precipitation((wait[WEATHER_CAT]))
        temp_x = np.concatenate([month, hour, day,  temp, precip])
        x.append(temp_x)
        y.append(self.__encode.encode_onehot_wait_time(round_to_nearest_five(wait[WAITTIME])))
    return x,y

  
  def get_data_encoded_std(self, data):
    x = []
    y = []

    for wait in data:
        month = self.__encode.encode_onehot_month(wait[MONTH])
        hour = self.__encode.encode_onehot_hour(wait[HOUR])
        day = self.__encode.encode_onehot_dow(wait[DOW])
        temp = self.__encode.encode_onehot_temp(wait[TEMP])
        precip = self.__encode.encode_onehot_precipitation((wait[WEATHER_CAT]))
        last_wait_time = self.__encode.encode_last_wait_time(wait[WAITTIME], self.__max_val)
        temp_x = np.concatenate([month, hour, day,  temp, precip])
        x.append(temp_x)
        y.append(self.__encode.analog_wait_time(wait[WAITTIME], self.__average, self.__standard_deviation, self.__min_val, self.__max_val))
    return x,y

  def get_data_averaged_hour(self, data):
    # TODO
    current_hour = data[0][HOUR]
    temp_hour_info = []
    new_data = []
    temp_val = []
    for wait in data:
      if current_hour != wait[HOUR]:
        list_temp = list(temp_val)
        list_temp[WAITTIME] = int(sum(temp_hour_info) / len(temp_hour_info))
        new_data.append(list_temp)
        temp_hour_info = []
        current_hour = wait[HOUR]
      temp_val = wait
      temp_hour_info.append(wait[WAITTIME])
    list_temp = list(temp_val)
    list_temp[WAITTIME] = sum(temp_hour_info) / len(temp_hour_info)
    new_data.append(list_temp)
    return new_data

  def get_data_by_day(self, data):
    # TODO 
    days = []
    current_day = []
    current_year = data[0][TIMESTAMP].year
    current_day_of_year = data[0][TIMESTAMP].timetuple().tm_yday
    for item in data:
      if current_year != item[TIMESTAMP].year or current_day_of_year != item[TIMESTAMP].timetuple().tm_yday:
        days.append(current_day)
        current_day = []
        current_year = item[TIMESTAMP].year
        current_day_of_year = item[TIMESTAMP].timetuple().tm_yday
      current_day.append(item)

    days.append(current_day)
    return days

  def prune_data_empty_days(self, data):
    new_days = []
    max_val = -1
    for item in data:
      if(max_val < len(item)):
        max_val = len(item)

    new_days = filter(lambda x: len(x) == max_val, data)
    return new_days

  def transform_from_lists_to_list(self, data):
    new_data = []
    for dat in data:
      new_data += dat
    return new_data


  def get_data_raw(self):
    return self.__raw_data

  def prune_data_hours(self, data, hours = [22,23,24,0,1,2,3,4,5,6,7]):
    new_data =[]
    for wait in data:
      if wait[HOUR] not in hours:
        new_data.append(wait)
    return new_data

  def get_time_series(self, data):
    time_series = []
    for item in data:
      time_series.append(float(item[WAITTIME]))
    return time_series

  def return_dataset_from_all(self, x, y):
    data_set_length = len(x)
    sixty_percent = int(data_set_length * self.__train_cutoff)
    eighty_percent = int(data_set_length * self.__val_cutoff)
    all_everyone = [[one, two] for one,two in zip(x,y)]
    random.shuffle(all_everyone)
    train = all_everyone[0:sixty_percent-1]
    val = all_everyone[sixty_percent:eighty_percent-1]
    test= all_everyone[eighty_percent:]
    train_x = np.array([t[0] for t in train])
    train_y = np.array([t[1] for t in train])
    val_x = np.array([t[0] for t in val])
    val_y = np.array([t[1] for t in val])
    test_x = np.array([t[0] for t in test])
    test_y = np.array([t[1] for t in test])
    return (train_x, train_y, test_x, test_y, val_x, val_y)


