import sys
from Config import Config
from Data import DataRepository
from AirQuality import AirData
from WeatherData import WeatherData
from NewWeatherData import NewWeatherData

config = Config.Config()
print("Config loaded")

max_rows_per_insert = 10000
repo = DataRepository.DataRepository(config.db_info, max_rows_per_insert)
print(repo.test_connection())


# Process wait time data if flag set
if("--wait" in sys.argv):
	print("Not implemented - Wait time data.")
	print("Probably not going to refactor this part.")
	
# Process air quality data if flag set
if("--air" in sys.argv):
	AirData.send_data_to_db(repo)

# Process Economic data if flag set
if("--econ" in sys.argv):
	print("Not implemented - Economic data")

# Process Oil/Gas data if flag set 
if("--petrol" in sys.argv):
	print("Not implemented - Oil/gas data")

# Process weather data
if("--weather" in sys.argv):
	WeatherData.send_data_to_db(repo)

if("--new_weather" in sys.argv):
	NewWeatherData.send_data_to_db(repo)
 

input("Completed succesfully")