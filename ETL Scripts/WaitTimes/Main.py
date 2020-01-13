import json
from datetime import datetime
from ../Config import Config
from ../DataRepository import DataRepository

rows_per_insert = 10000
config = Config()
repo = DataRepository(config.db_info, rows_per_insert)


print("Loading data file...")
startTime = datetime.now()
with open('wait_times.json', 'r') as datafile:
    data = json.loads(datafile.read())
endTime = datetime.now()
print(f"Loaded data from file. Took {str(endTime - startTime)}")


print("Formatting queries...")
startTime = datetime.now()
queries = repo.format_wait_time_data(data)
endTime = datetime.now()
print(f"Formatted data into {len(queries)} inserts of {rows_per_insert} rows each. Took {str(endTime - startTime)}")


print("Executing queries...")
startTime = datetime.now()
counter = 0
for query in queries:
	counter = counter + 1
	print(f'\t- Executing query #{counter}')
	repo.execute_query(query)
endTime = datetime.now()
print(f'Queries all executed! Took {str(endTime - startTime)}')
