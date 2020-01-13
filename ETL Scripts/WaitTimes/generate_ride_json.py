import json

data = json.load(open('rides.json', 'r'))

new_ride_data = {}

for ride in data['kept']:
    new_ride_data[ride[1]] = {'outdoor': None, 'speed' : -1, 'music': -1, 'dark': -1, 'water': -1, 'coaster': None, 'car': None, 'train': None, 'spinner': None, 'isshow': None, 'story': None, 'game': None, 'simulation': None}
	
with open('new_ride_data.json', 'w') as outfile:
    json.dump(new_ride_data, outfile)