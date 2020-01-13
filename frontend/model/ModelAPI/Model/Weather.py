from datetime import datetime, timedelta
import requests


def get_weather_data(timestamp):
    weather_data_key = "a81d7bd0d10afeff2f85de3367189a91"
    p_end = "weather/"
    f_end = "forecast/"
    base_weather_URL = "http://api.openweathermap.org/data/2.5/"
    city = "Orlando,US"
    url = base_weather_URL
    result = {}
    if timestamp <= datetime.now():
        url = url + p_end
        url = url + f"?q={city}&APPID={weather_data_key}"
        response = requests.get(url).json()
        # parse as normal 
        result = parse_weather_object(response)
    else:
        url = url + f_end
        url = url + f"?q={city}&APPID={weather_data_key}"
        # Need to iterate through returned object and parse unix string to date time
        # Then can parse as normal
        response = requests.get(url).json()
        data = response["list"]
        for forecast in data:
            dt = datetime.utcfromtimestamp(forecast["dt"])
            # Match by date, and hour, ignore everything else 
            if dt >= timestamp and dt < timestamp + timedelta(hours=3):
                result = parse_weather_object(forecast)
                break
    return result 

def parse_weather_object(data):
    result = {}
    main = data["main"]
    wind = data["wind"]
    weather = data['weather'][0] # Only take the first row in this array
    result["temp"] = main["temp"]
    result["temp_min"] = main["temp_min"]
    result["temp_max"] = main["temp_max"]
    result["pressure"] = main["pressure"]
    result["humidity"] = main["humidity"]
    result["wind_speed"] = wind["speed"]
    result["weather_main"] = weather["main"]
    result["weather_description"] = weather["description"]
    return result