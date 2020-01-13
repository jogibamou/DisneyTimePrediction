import json 
import datetime as dt

table_name = 'weather_data2'
column_names = ['timestamp', 'temp', 'temp_min', 'temp_max', 'pressure', 'humidity', 'wind_speed', 'weather_main', 'weather_description']

def __load_data__():
	data = {}
	with open('NewWeatherData/new-weather-data_2012-2019.json') as jsondata:
		data = json.loads(jsondata.read())
	return data


def send_data_to_db(repo):
	# Load data from file 
	print("Loading data from file")
	jsondata = __load_data__()
	# Parse into rows matching column names
	print("Parsing data into json")
	rows = []
	for datum in jsondata:
		main = datum['main']
		wind = datum['wind']
		weather = datum['weather'][0] # Only take the first row in this array
		timestamp = dt.datetime.utcfromtimestamp(datum['dt']).strftime('%Y-%m-%d %H:%M:%S -00:00') # Parse epoch time rather than re-parse the string carried along with it
		temp = main['temp']
		temp_min = main['temp_min']
		temp_max = main['temp_max']
		pressure = main['pressure']
		humidity = main['humidity']
		wind_speed = wind['speed']
		weather_main = weather['main']
		weather_description = weather['description']

		r = [f'$${timestamp}$$']
		r.append(f'$${temp}$$')
		r.append(f'$${temp_min}$$')
		r.append(f'$${temp_max}$$')
		r.append(f'$${pressure}$$')
		r.append(f'$${humidity}$$')
		r.append(f'$${wind_speed}$$')
		r.append(f'$${weather_main}$$')
		r.append(f'$${weather_description}$$')
		rows.append(r)


	print("Calling repository data insert function")
	repo.insert_rows_into_table(table_name, column_names, rows)	
