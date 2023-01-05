import pandas as pd
from IPython.display import display
import requests
import argparse


parser = argparse.ArgumentParser(description='Generate CSV of weather data for a city')
parser.add_argument('-c', '--city', default='madrid', help='City to obtain the weather from')
args = parser.parse_args()

columns_names = ['city', 'aqi', 'iaqi_h', 'iaqi_p', 'iaqi_pm10', 'iaqi_t', 'date',
                'o3_avg', 'o3_max', 'o3_min', 'pm10_avg', 'pm10_max', 'pm10_min',
                'pm25_avg', 'pm25_max', 'pm25_min', 'uvi_avg', 'uvi_max', 'uvi_min']

#Get the Madrid air quality data from the API
wanted_city = args.city 
API = "http://api.waqi.info/feed/" + wanted_city + "/?token=19e67e8766e1e01fe3ee85f2ab73f5a6d41868ee"
air_quality = requests.get(API).json()
air_quality_data = air_quality["data"]

air_df = pd.DataFrame(columns=columns_names)
row1 = []
row1.append(air_quality_data['city']['name'])#city
row1.append(air_quality_data['aqi'])#aqi
row1.append(air_quality_data['iaqi']['h']['v'])#iaqi_h
row1.append(air_quality_data['iaqi']['p']['v'])#iaqi_p
row1.append(air_quality_data['iaqi']['pm10']['v'])#iaqi_pm10
row1.append(air_quality_data['iaqi']['t']['v'])#iaqi_t

keys = list( air_quality_data['forecast']['daily'].keys() )
o3 = air_quality_data['forecast']['daily'][keys[0]]
pm10 = air_quality_data['forecast']['daily'][keys[1]]
pm25 = air_quality_data['forecast']['daily'][keys[2]]
uvi = air_quality_data['forecast']['daily'][keys[3]]

if len(uvi) != len(o3):
    uvi = uvi * len(o3)

for i, day in enumerate(zip(o3, pm10, pm25, uvi)):
    row2 = []
    row2.append(day[0]['day'])
    for dict in day:
        row2.append(dict['avg'])
        row2.append(dict['max'])
        row2.append(dict['min'])
    
    row = row1 + row2
    
    air_df.loc[i] = row
    
#Convert air_df in .csv and save it
file_name = f"help_data/air_{args.city}.csv"
air_df.to_csv(file_name, sep=',', index=False)
    

    
    


