import pandas as pd
import numpy as np
import hopsworks
import os 
# from dotenv import load_dotenv
import requests
import json
import datetime
import urllib.request
import codecs
import csv
import sys
from functions import *

DEFAULT_CITY = "MADRID"


AQ_COL_NAMES = ['city', 'aqi', 'iaqi_h', 'iaqi_p', 'iaqi_pm10', 'iaqi_t', 'date',
                'o3_avg', 'o3_max', 'o3_min', 'pm10_avg', 'pm10_max', 'pm10_min',
                'pm25_avg', 'pm25_max', 'pm25_min']


WEATHER_COL_NAMES = ["name","datetime","tempmax","tempmin","temp","feelslikemax","feelslikemin","feelslike",
            "dew","humidity","precip","precipprob","precipcover","snow","snowdepth","windgust","windspeed","winddir",
            "sealevelpressure","cloudcover","visibility","solarradiation","solarenergy","uvindex","conditions"
            ]

WEATHER_COL_RENAMES = {"name":"city", "datetime":"date", "sealevelpressure":"pressure"}


def get_air_df(api_key, city, index=0, save_=False):
    aq_data = requests.get(f'https://api.waqi.info/feed/{city}/?token={api_key}').json()['data']

    if save_:
        json_string = json.dumps(aq_data)
        with open("help/json_data.json", "w") as outfile:
            outfile.write(json_string)

    forecast = aq_data['forecast']['daily']

    air_df = pd.DataFrame(columns=AQ_COL_NAMES)
    row = []
    row.append(aq_data['city']['name'])#city
    row.append(aq_data['aqi'])#aqi
    row.append(aq_data['iaqi']['h']['v'])#iaqi_h
    row.append(aq_data['iaqi']['p']['v'])#iaqi_p
    row.append(aq_data['iaqi']['pm10']['v'])#iaqi_pm10
    row.append(aq_data['iaqi']['t']['v'])#iaqi_t
    row.append(forecast['o3'][index]['day']) # Current day
    row.append(forecast['o3'][index]['avg'])
    row.append(forecast['o3'][index]['max'])
    row.append(forecast['o3'][index]['min'])
    row.append(forecast['pm10'][index]['avg'])
    row.append(forecast['pm10'][index]['max'])
    row.append(forecast['pm10'][index]['min'])
    row.append(forecast['pm25'][index]['avg'])
    row.append(forecast['pm25'][index]['max'])
    row.append(forecast['pm25'][index]['min'])

    air_df.loc[index] = row

    return air_df


def get_weather_df(api_key, city, index=0):
    
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d")

    city = DEFAULT_CITY.lower()


    try: 
        ResultBytes = urllib.request.urlopen(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{now}/{now}?unitGroup=metric&include=days&key={api_key}&contentType=csv")
        # Parse the results as CSV
        data = codecs.iterdecode(ResultBytes, 'utf-8')

        CSVText = csv.reader(data)
        

    except urllib.error.HTTPError  as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except  urllib.error.URLError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code,ErrorInfo)
        sys.exit()



    df = pd.DataFrame(data=CSVText)
    df = df.rename(columns=df.iloc[0])
    df = df.drop([0])
    df = df.reset_index(drop=True)
    df = df[WEATHER_COL_NAMES]
    df = df.rename(columns=WEATHER_COL_RENAMES)

    return df





if __name__ == "__main__":
    # load_dotenv()
    # AIR_QUALITY_API_KEY = os.getenv("AIR_QUALITY_API_KEY")
    # WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


    AIR_QUALITY_API_KEY = os.environ.get("AIR_QUALITY_API_KEY")
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
    HOPWSORKS_API_KEY = os.environ.get("HOPSWORKS_API_KEY")


    df_air = get_air_df(AIR_QUALITY_API_KEY, DEFAULT_CITY, save_=False)

    df_weather = get_weather_df(WEATHER_API_KEY, DEFAULT_CITY)

    # Apply date function
    df_air["date"] = df_air["date"].apply(timestamp_2_time)
    df_weather["date"] = df_weather["date"].apply(timestamp_2_time)

    # print(df_air)
    # print(df_weather)

    project = hopsworks.login()

    fs = project.get_feature_store() 

    air_quality_fg = fs.get_or_create_feature_group(
        name = 'air_quality_fg',
        version = 1
    )
    weather_fg = fs.get_or_create_feature_group(
        name = 'weather_fg',
        version = 1
    )


    # air_quality_fg.insert(df_air)
    # weather_fg.insert(df_weather)
    

