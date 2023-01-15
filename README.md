# id2223_project

# Air Quality - Madrid

## Authors:
### - Jorge Santiago Roman Avila : jsra2@kth.se
### - Carlo Saccardi: saccardi@kth.se
<br>

This project is for the course __ID2223 Scalable Machine Learning__ offered at __KTH Royal Institute of Technology__. 

It is a prediction service for the Air Quality Index for the city of Madrid, based on daily weather statistics.
The prediction model is trained on tabular data from a day, and predicts the air quality index of the next day. 

Data was recollected from the open data sources:
- Air Quality API : https://aqicn.org/api/
- Weather API : https://www.visualcrossing.com/weather-api 

The files in this repository are the different modules for the development of the project.
- The files *air_cvs.py* and *weather_csv.py* are auxilary files to help create the CSVs that will act as backfill historical data for both feature groups. 
- The file *backfill.py* then creates 2 feature groups, based on these past CSVs. 
- The file *feature_pipeline.py* is a file that is run scheduled on Github Actions every day. It gets daily the new AQ and weather statistics for the day for Madrid, and inserts them into the respective Hopsworks Feature Group. 
- The notebook *feature_views.ipynb* is a notebook that gets both feature groups, and joins them to produce a feature view. This feature view is scaled ready to serve as training data for a model, and also to give out data for daily inference.
- The notebook *model_training.ipynb* is a notebook that creates a training dataset from the feature view, and trains an XGB Regressor model to predict the next day AQI. 
- The file *inference_pipeline.py* is a file that from the feature view and the currently trained model, gets the daily data and makes a prediction for the next day, and updates a feature group in hopsworks, with the latest prediction for that day. This file is also ran on a schedule by Github Actions, and is ran 15 minutes after the feature pipeline updates the feature groups with the latest data. 
- The file _app.py_ is a Gradio App that reports tomorrow's AQI for Madrid, and also gives a description of the quality and recommendations based on the prediction value. 


Huggingface interface is found in :