import json


data = json.load(open('new_ride_data.json', 'r'))

outdoor = 'outdoor'
speed = 'speed'
music = 'music'
dark = 'dark'
water = 'water'
coaster = 'coaster'
car = 'car'
train = 'train'
spinner = 'spinner'
isshow = 'isshow'
story = 'story'
game = 'game'
simulation = 'simulation'
str = ''
for i in data.keys():
    str += f'SELECT $Warehouse$.$modify_attraction$(${i}$, {data[i][outdoor]}, {data[i][speed]}, {data[i][music]}, {data[i][dark]}, {data[i][water]}, {data[i][coaster]}, {data[i][car]}, {data[i][train]}, {data[i][spinner]}, {data[i][isshow]}, {data[i][story]}, {data[i][game]}, {data[i][simulation]});\n'
    
with open('quick_mod_attraction_script.txt', 'w') as outfile:
    outfile.write(str)
    outfile.close()