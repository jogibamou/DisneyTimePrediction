import json 

table_name = 'weather_data'
column_names = ['station_name', 'date', 'precipitation', 'temp_avg', 'temp_max', 'temp_min']

def __load_data__():
	data = {}
	with open('WeatherData/NOAAData.json') as jsondata:
		data = json.loads(jsondata.read())
	return data

def send_data_to_db(repo):
	# Load data from file 
	print("Loading data from file")
	jsondata = __load_data__()
	# Parse into rows matching column names
	print("Parsing data into json")
	rows = []
	for station in jsondata:
		name = station["NAME"]
		for datum in station["DATA"]:
			# Build row here
			r = [f"$${name}$$"] 
			r.append(f"$${datum['DATE']}$$")
			precip = datum['PRCP'] if datum['PRCP'] != "" else 0
			r.append(f"$${precip}$$")
			r.append(f"$${datum['TAVG']}$$" if datum['TAVG'] != "" else "NULL")
			r.append(f"$${datum['TMAX']}$$" if datum['TMAX'] != "" else "NULL")
			r.append(f"$${datum['TMIN']}$$" if datum['TMIN'] != "" else "NULL")
			# Add row to rows 
			rows.append(r)
	# Call repo insert function
	print("Calling repository data insert function")
	repo.insert_rows_into_table(table_name, column_names, rows)	




	# for location, values in jsondata.items():
	# 	for keys, data in values.items():
	# 		for row in data:
	# 				r = []
	# 				r.append(f'$${location}$$')
	# 				r.append(f'$${row["CSBA Code"]}$$')
	# 				r.append(f'$${row["Date"]}$$')
	# 				r.append(f'$${row["AQI"]}$$')
	# 				r.append(f'$${row["Category"]}$$')
	# 				r.append(f'$${row["Defining Parameter"]}$$')
	# 				rows.append(r)
	# 				# Not using 'Number of Sites Reporting'
