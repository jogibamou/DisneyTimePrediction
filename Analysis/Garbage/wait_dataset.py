from DatasetAPI import Datasets
from enum import Enum
import numpy as np
import math
# Step 1 get all the data raw
# Step 2 create a dataset

# The first thing in a row from attractions that matters
attraction_id_index = 0
attraction_start_index = 4

# The indices in wait times that matter
wait_time_id_index = 0
wait_time_attraction_index = 1
wait_time_date = 2
wait_time_actual_time = 3

# The indices for regined attractions


# The indices for refined wait times
_wait_time_attraction_index = 0
_wait_time_month = 1
_wait_time_hour = 2
_wait_time_actual_time = 3

# Max wait time
max_wait_time = 400
wait_time_increment = 5

# Metadata for max values in integer
max_speed = 4
max_music = 3
max_dark = 3
max_water = 4



class InputSetup(Enum):
    OUTDOOR = 0, # Start after 12 months and 12 2 hour increments
    SPEED = 1,
    MUSIC = 2,
    DARK = 3,
    WATER = 4,
    COASTER = 5,
    CAR = 6,
    TRAIN = 7,
    SPINNER = 8, 
    ISSHOW = 9,
    STORY = 10,
    GAME = 11,
    SIMULATION = 12,
    PARKOPEN = 13,
    MONTH = 14,
    HOUR = 15
    

def create_data_set(attraction_rows, waittime_rows):
     # Step 2.1 Create attraction dictionary
     attractions = create_attraction_dictionary(attraction_rows)
     # Step 2.2 Create formatted wait time list
     wait_times = refine_waittime_rows(waittime_rows)

     x = []
     y = []
     for wait in wait_times:
         temp_x = []
         temp_x.extend(attractions[wait[_wait_time_attraction_index]])
         temp_x.append(wait[_wait_time_month])
         temp_x.append(wait[_wait_time_hour])
         x.append(np.array(convert_x_row(temp_x)))
         temp_y = wait[_wait_time_actual_time] // wait_time_increment
         y.append(temp_y)
     return x,y

def convert_x_row(x_row):
    con_x_row = []
    # Outdoor
    con_x_row.append(convert_bool(x_row[0]))
    # Speed
    con_x_row.append(convert_float(x_row[1], max_speed))
    # Music
    con_x_row.append(convert_float(x_row[2], max_music))
    # Dark
    con_x_row.append(convert_float(x_row[3], max_dark))
    # Water
    con_x_row.append(convert_float(x_row[4], max_water))
    # Rest are bools
    for item in x_row[5:]:
        con_x_row.append(convert_bool(item))
    return con_x_row


def convert_bool(val):
    if val == True:
        return 1.0
    else:
        return 0.0

def convert_float(val, max_val):
    return val / max_val

# Step 2.1
def create_attraction_dictionary(attraction_rows):
    attractions = {}
    for row in attraction_rows:
        attractions[row[attraction_id_index]] = []
        attractions[row[attraction_id_index]].extend(row[attraction_start_index:])
    return attractions

def refine_waittime_rows(waittime_rows):
    new_waittime_rows = []
    for row in waittime_rows:
        new_waittime_rows.append([row[wait_time_attraction_index], row[wait_time_date].month, row[wait_time_date].hour, row[wait_time_actual_time]])
    return new_waittime_rows


def get_wait_data(_limit = 100):
    data = Datasets.DataAccessor()
    attraction_rows =  data.get('Warehouse', 'Attractions', limit = 100)
    attraction_wait = data.get('public', 'filtered_wait_times',limit = _limit) 
    x,y = create_data_set(attraction_rows, attraction_wait)

    eighty_percent = math.floor(len(x) * .8)
    train_x = x[:eighty_percent]
    train_y = y[:eighty_percent]
    test_x = x[eighty_percent:]
    test_y = y[eighty_percent:]

    return np.array(train_x), np.array(train_y), np.array(test_x), np.array(test_y)

