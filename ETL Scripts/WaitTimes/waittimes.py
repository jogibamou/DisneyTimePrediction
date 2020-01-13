import os
import pandas as pd
import json
import numpy as np
import math
import time
import requests

park_folder = {"animal_kingdom" : "AKWT", "epcot" : "EWT", "hollywood_studios" : "HSWT", "magic_kingdom" : "MKWT"}
rides = {'lost' : [], 'kept' : []}
# Function for getting list of all files 
def get_files():
    files = {}
    for key in park_folder.keys():
       s = os.getcwd() + "\\" + park_folder[key]
       print(s)
       files[key] = os.listdir(s)
    return files

def get_frames(folder, files):
    frames = []
    count = 0
    for file in files:
        temp_frame = pd.read_excel(os.getcwd() + "\\" + folder + "\\" + file)
        print("Got frame in " + folder + "\\" + file)
        frames.append(temp_frame)
        #return frames
    print('Got Frames')
    return frames

def get_columns(frames):
    columns = np.array([])
    for frame in frames:
        columns = np.union1d(columns, frame.columns[1:])
    column_dict = {}
    for col in columns:
       if col.find("Unnamed") == -1:
           col = convert_col(col)
           column_dict[col] = []
    return column_dict
    
def fill_json(frames, park_data, key):
    for frame in frames[key]:
        for row in frame.values:
           temp_row = row[find_date(row):]
           for val, col in zip(temp_row[1:], frame.columns[1:]):
               col = convert_col(col)
               if col in park_data[key].keys():
                    park_data[key][col].append({"timestamp" : temp_row[0], "wait_time" : val if not math.isnan(val) else -1})
            

def find_date(row):
    for item, num in zip(row, range(0,len(row))):
       if isinstance(item,str):
          return num
          
def count_data(park_data):
    zero_time = 0
    more_time = 0
    for key in list(park_data.keys()):
        for key2 in list(park_data[key].keys()):
            for item in park_data[key][key2]:
                if item['wait_time'] > 0:
                    more_time = more_time + 1
                else:
                    zero_time = zero_time + 1
    print("Zero Time " + str(zero_time))
    print("More Time " + str(more_time))


def prune(park_data):
    keys_remove= []
    for key in park_data.keys():
        for attraction in park_data[key].keys():
            print(attraction)
            good_time = False
            for dat in park_data[key][attraction]:
                if dat['wait_time'] > 0:
                    if not good_time:
                        rides['kept'].append([key, attraction])
                    good_time = True
            if not good_time:
                keys_remove.append([key, attraction])
    
    for rm in keys_remove:
        rides['lost'].append([rm[0], rm[1]])
        del park_data[rm[0]][rm[1]]


def convert_col(col):
       if col.find('-') != -1:
           return col[:col.find('-') - 1]
       elif col.find('–') != -1:
            return col[:col.find('–') - 1]
       else:
            return col
# Get all the files 
files = get_files()

# Begin the jsonization
park_data = {}
frames = {}
for key in park_folder.keys():
    print(f'processing key {key}')
    frames[key] = get_frames(park_folder[key], files[key])
    park_data[key] = get_columns(frames[key])
    fill_json(frames, park_data, key)
#print(park_data['animal_kingdom']['Affection Section'][0:10])
#print(park_data['animal_kingdom']['Affection Section'][3500:3510])
count_data(park_data)
prune(park_data)
count_data(park_data)
# Send via request rather than save to file
with open('wait_times.json', 'w') as outfile:
   json.dump(park_data, outfile)
   outfile.close()

with open('rides.json', 'w') as outfile2:
   json.dump(rides, outfile2)
   outfile2.close()
'''
files = get_files()
frame = pd.read_excel(os.getcwd() + "\\" + park_folder["animal_kingdom"] + "\\" + files["animal_kingdom"][0])    
print(frame)
print(frame.columns[1:])
print(frame.values.shape)
print(frame.values)
print("Try again")
print(frame.values[:,1:])
'''