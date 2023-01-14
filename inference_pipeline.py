import pandas as pd
import numpy as np
import hopsworks
import os 

from functions import *

import joblib
import xgboost as xgb

import warnings
warnings.filterwarnings("ignore")



if __name__== "__main__":
    project = hopsworks.login()
    fs = project.get_feature_store() 

    air_columns_names = ['aqi', 'iaqi_h', 'iaqi_p', 'iaqi_pm10', 'iaqi_t', 'date',
                    'o3_avg', 'o3_max', 'o3_min', 'pm10_avg', 'pm10_max', 'pm10_min',
                    'pm25_avg', 'pm25_max', 'pm25_min']


    HOPWSORKS_API_KEY = os.environ.get("HOPSWORKS_API_KEY")


    feature_view = fs.get_feature_view(
        name = 'air_quality_fv',
        version = 6
    )


    today_date = datetime.now() - timedelta(days=1)
    today_date = today_date.strftime("%Y-%m-%d")
    today_date = timestamp_2_time(today_date)
    # today_vector = feature_view.get_feature_vector({"date": today_date})

    # print(today_vector)

    batch_data = feature_view.get_batch_data(start_time=today_date)

    batch_data = batch_data.sort_values(by = ['date'], ignore_index = True)
    

    batch_data = batch_data.iloc[-1:]
    

    today_date = batch_data["date"]
    
    batch_data = batch_data.drop(columns=["date"])
    
    tomorrow_date = datetime.fromtimestamp(today_date//1000) + timedelta(days=1)
    tomorrow_date = tomorrow_date.strftime("%Y-%m-%d")
    tomorrow_date = timestamp_2_time(tomorrow_date)
    
    mr = project.get_model_registry()
    model = mr.get_model("xgboost_model", version=4)
    model_dir = model.download()
    model = joblib.load(model_dir + "/model.pkl")

    # print(batch_data)
    y_pred = model.predict(batch_data)
    # print(y_pred)
    # print(y_pred[0])

    monitor_fg = fs.get_or_create_feature_group(name="air_quality_predictions",
                                                version=2,
                                                primary_key=["date"],
                                                description="Air quality predictions"
                                                )


    df_pred = pd.DataFrame({"date": today_date, "tomorrow_date": tomorrow_date, "pred_aqi":y_pred})
    # print(df_pred)
    monitor_fg.insert(df_pred)