# Prediction model code
from tensorflow import keras
from os import listdir
from os.path import isfile, join
from datetime import datetime
from Model import Weather, Encoding 
import numpy as np


rides = {

        "dwarfs":{"name" : "Seven Dwarfs Mine Train" , "schema" : "public" , "material" : "dwarves_data", "avg" : 82.03, "std" : 33.85, "min" : 0, "max": 300},
        "alien":{"name" : "Alien Swirling Saucers" , "schema" : "public" , "material" : "alien_data", "avg" : 36.87, "std" : 16.34, "min" : 0, "max" : 190},
        "dinosaur":{"name" : "Dinosaur" , "schema" : "public" , "material" : "dinoasur_data", "avg" : 25.98, "std" : 18.55, "min" : 0, "max" : 300},
        "expedition":{"name" : "Expedition Everest" , "schema" : "public" , "material" : "expedition_everest_data", "avg" : 31.97, "std": 21.84, "min" : 0, "max": 180}, 
        "navi":{"name" : "Na’vi River Journey" , "schema" : "public" , "material" : "navi_data", "avg" : 75.08, "std" : 31.61, "min" : 0, "max": 225},
        "rockn_roller":{"name" : "Rock 'n' Roller Coaster Starring Aerosmith" , "schema" : "public" , "material" : "rockn_roller_coaster", "avg": 59.09, "std": 31.73, "min":0, "max":250},
        "soarin":{"name" : "Soarin'" , "schema" : "public" , "material" : "soarin_data2", "avg": 53.88, "std":29.49, "min":0, "max":280},
        "spaceship_earth":{"name" : "Spaceship Earth" , "schema" : "public" , "material" : "spaceship_earth_data", "avg":17.65, "std":14.26, "min":0, "max":210},
        "splash_mountain":{"name" : "Splash Mountain" , "schema" : "public" , "material" : "splash_mountain_data", "avg" : 42.42, "std" : 30.11, "min" : 0, "max" : 300 },
        "thunder_mountain":{"name" : "Big Thunder Mountain Railroad" , "schema" : "public" , "material" : "filtered_thundermountain_weather2", "avg" : 26.98, "std" : 29.72, "min" : 0, "max" : 190}
}

class PredictionModel:
    def __init__(self,datafolder):
        self.E = Encoding.Encoding()
        self.models = {}
        self.max_times = {}
        names = [file for file in listdir(datafolder) if isfile(join(datafolder, file))]
        for name in names:
            print(f"Loading {name}")
            m = keras.models.Sequential([
            keras.layers.Input((72,), name="begin"), 
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.Dense(1, activation= 'sigmoid')
            ])
            m.compile(optimizer = 'adam', loss = keras.losses.Poisson())
            m.load_weights(f"{datafolder}/{name}")
            m.load_weights(datafolder+"/"+name)
            self.models[rides[name[:name.index(".")]]["name"]] = m
            self.max_times[rides[name[:name.index(".")]]["name"]] = rides[name[:name.index(".")]]["max"]
        # Open all files and reacreate models for each ride in dictionary 
    

    def predict(self,timestamp, park, ride):
        model = self.models[ride]

        x = []

        weather = Weather.get_weather_data(timestamp)
        # Month
        month = self.E.encode_onehot_month(int(timestamp.strftime('%m')))
        # hour
        hour = self.E.encode_onehot_hour(int(timestamp.strftime('%H')))
        # DOW
        dow = self.E.encode_onehot_dow(timestamp.weekday())
        # temp
        temp = self.E.encode_onehot_temp(weather["temp"])
        w = ""
        # Weather cat
        if (weather["weather_main"]) in ("Rain", "Thunderstorm"):
            w = weather["weather_description"]
        else:
            w = weather["weather_main"]
        precip = self.E.encode_onehot_precipitation(w)
        x = np.concatenate((month, hour, dow, temp, precip))
        prediction = self.models[ride].predict(np.array([x]))
        return prediction * self.max_times[ride]

    def test(self,array):
        ride = "Expedition Everest"
        return self.models[ride].predict(np.array([array])) * self.max_times[ride]


