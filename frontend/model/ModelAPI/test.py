from Model import Model, Weather
from datetime import datetime, timedelta

print(Weather.get_weather_data(datetime.now()))
print(Weather.get_weather_data(datetime.now() + timedelta(days=3)))
