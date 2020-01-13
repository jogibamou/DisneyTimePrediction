import json 

table_name = 'air_quality_buffer'
column_names = ['location_name', 'csba_code', 'date', 'aqi', 'category', 'defining_parameter']

def __load_data__():
	data = {}
	with open('AirQuality/daily_air_quality_data.json') as jsondata:
		data = json.loads(jsondata.read())
	return data

def send_data_to_db(repo):
	# Load data from file 
	print("Loading data from file")
	jsondata = __load_data__()
	# Parse into rows matching column names
	print("Parsing data into json")
	rows = []
	for location, values in jsondata.items():
		for keys, data in values.items():
			for row in data:
					r = []
					r.append(f'$${location}$$')
					r.append(f'$${row["CSBA Code"]}$$')
					r.append(f'$${row["Date"]}$$')
					r.append(f'$${row["AQI"]}$$')
					r.append(f'$${row["Category"]}$$')
					r.append(f'$${row["Defining Parameter"]}$$')
					rows.append(r)
					# Not using 'Number of Sites Reporting'
	# Call repo insert function
	print("Calling repository data insert function")
	repo.insert_rows_into_table(table_name, column_names, rows)