import pandas as pd
import numpy as np
import os 
from dotenv import load_dotenv
from pathlib import Path
import requests
import json
import csv
import urllib.request
import sys
import codecs
import argparse
import datetime

CITIES = ["Madrid", "Barcelona", "Valencia", "Sevilla"]


COL_NAMES = ["name","datetime","tempmax","tempmin","temp","feelslikemax","feelslikemin","feelslike",
            "dew","humidity","precip","precipprob","precipcover","snow","snowdepth","windgust","windspeed","winddir",
            "sealevelpressure","cloudcover","visibility","solarradiation","solarenergy","uvindex","conditions"
            ]

COL_RENAMES = {"name":"city", "datetime":"date", "sealevelpressure":"pressure"}



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate CSV of weather data for a city')
    parser.add_argument('-c', '--city', default='madrid', help='City to obtain the weather from')
    parser.add_argument('-sd', '--start_date', default='2022-12-01', help='Start date to obtain the weather from')
    parser.add_argument('-ed', '--end_date', default=None, help='End date to obtain the weather from')

    args = parser.parse_args()

    if args.end_date is None:
        
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d")

        args.end_date = now


    load_dotenv()
    

    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")



    try: 
        ResultBytes = urllib.request.urlopen(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{args.city}/{args.start_date}/{args.end_date}?unitGroup=metric&include=days&key={WEATHER_API_KEY}&contentType=csv")
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



    file_name = f"help_data/weather_{args.city}.csv"

    file = codecs.open(file_name, "w", "utf-8")
    file.write(''.join(data))
    file.close()


    df = pd.read_csv(file_name, header=0)

    df = df[COL_NAMES]
    df = df.rename(columns=COL_RENAMES)

    df.to_csv(file_name, index=False)



    




    

