import pandas as pd
import numpy as np
import os 
from dotenv import load_dotenv
from pathlib import Path
import requests
import json


CITIES = ["Madrid", "Barcelona", "Valencia", "Sevilla"]


COL_NAMES = ['city','aqi','date','iaqi_h','iaqi_p','iaqi_pm10',
             'iaqi_t','o3_avg','o3_max','o3_min','pm10_avg',
             'pm10_max','pm10_min','pm25_avg','pm25_max',
             'pm25_min','uvi_avg','uvi_max','uvi_min'
            ]


def get_air_df(api_key, city, index=0, save_=False):
    json_ = requests.get(f'https://api.waqi.info/feed/{city}/?token={api_key}').json()['data']

    if save_:
        json_string = json.dumps(json_)
        with open("help/json_data.json", "w") as outfile:
            outfile.write(json_string)

    iaqi = json_['iaqi']
    forecast = json_['forecast']['daily']

    values = [  json_['aqi'],              
                json_['time']['s'][:10],     
                iaqi['h']['v'],
                iaqi['p']['v'],
                iaqi['pm10']['v'],
                iaqi['t']['v'],
                forecast['o3'][index]['avg'],
                forecast['o3'][index]['max'],
                forecast['o3'][index]['min'],
                forecast['pm10'][index]['avg'],
                forecast['pm10'][index]['max'],
                forecast['pm10'][index]['min'],
                forecast['pm25'][index]['avg'],
                forecast['pm25'][index]['max'],
                forecast['pm25'][index]['min'],
                forecast['uvi'][index]['avg'],
                forecast['uvi'][index]['avg'],
                forecast['uvi'][index]['avg']]

    data = dict.fromkeys(COL_NAMES)

    df = None

    return json_


def get_weather_df(api_key, city):



    pass


if __name__ == "__main__":
    load_dotenv()
    AIR_QUALITY_API_KEY = os.getenv("AIR_QUALITY_API_KEY")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")




    df_air = get_air_df(AIR_QUALITY_API_KEY, "Madrid", save_=True)


    print(df_air)

    

