import pandas as pd
import numpy as np
import os 
from dotenv import load_dotenv
from pathlib import Path
import requests
import json
import argparse
import datetime
from functions import *
import hopsworks


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
    parser = argparse.ArgumentParser(description='Backfill the default ')
    parser.add_argument('-c', '--city', default='madrid', help='City to obtain the weather from')
    parser.add_argument('-sd', '--start_date', default='2023-01-01', help='Start date to obtain the weather from')
    parser.add_argument('-ed', '--end_date', default=None, help='End date to obtain the weather from')

    args = parser.parse_args()


    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Backfill with CSVs ')
    parser.add_argument('-aq', '--air-quality', default='air_madrid.csv', help='CSV file where the air quality backfill is')
    parser.add_argument('-w', '--weather', default='weather_madrid.csv', help='CSV file where the weather backfill is')

    args = parser.parse_args()


    aq_path = os.path.join("help_data", args.air_quality)
    weather_path = os.path.join("help_data", args.weather)


    df_aq = pd.read_csv(aq_path)
    df_weather = pd.read_csv(weather_path)
    

    # Apply date function
    df_aq["date"] = df_aq["date"].apply(timestamp_2_time)
    df_weather["date"] = df_weather["date"].apply(timestamp_2_time)

    
    # Sort 
    df_aq = df_aq.sort_values(by = ['date'], ignore_index = True)
    df_weather = df_weather.sort_values(by = ['date'], ignore_index = True)


    # Hopsworks
    project = hopsworks.login()
    fs = project.get_feature_store() 


    # Create Feature Group
    aq_fg = fs.get_or_create_feature_group(
        name = 'air_quality_fg',
        description = 'Air Quality characteristics of each day',
        version = 1,
        primary_key = ['city','date'],
        online_enabled = True,
        event_time = 'date'
    )    

    aq_fg.insert(df_aq)

    weather_fg = fs.get_or_create_feature_group(
        name = 'weather_fg',
        description = 'Weather characteristics of each day',
        version = 1,
        primary_key = ['city','date'],
        online_enabled = True,
        event_time = 'date'
    )    

    weather_fg.insert(df_weather)
    

