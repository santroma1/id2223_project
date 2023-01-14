import pandas as pd
import numpy as np
import hopsworks
import os 

from functions import *


import xgboost as xgb

import warnings
warnings.filterwarnings("ignore")



if __name__== "__main__":
    project = hopsworks.login()
    fs = project.get_feature_store() 

    air_columns_names = ['city', 'aqi', 'iaqi_h', 'iaqi_p', 'iaqi_pm10', 'iaqi_t', 'date',
                    'o3_avg', 'o3_max', 'o3_min', 'pm10_avg', 'pm10_max', 'pm10_min',
                    'pm25_avg', 'pm25_max', 'pm25_min']


    HOPWSORKS_API_KEY = os.environ.get("HOPSWORKS_API_KEY")


    feature_view = fs.get_feature_view(
        name = 'air_quality_fv',
        version = 5
    )


    today_date = datetime.now()
    today_date = today_date.strftime("%Y-%m-%d")
    today_date = timestamp_2_time(today_date)
    today_vector = feature_view.get_feature_vector({"date": today_date})

    print(today_vector)
