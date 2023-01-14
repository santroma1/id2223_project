import gradio as gr
import numpy as np
from PIL import Image
import requests

import hopsworks
import joblib

project = hopsworks.login()
fs = project.get_feature_store()


mr = project.get_model_registry()
model = mr.get_model("air_quality_predictions", version=2)
model_dir = model.download()
model = joblib.load(model_dir + "/air_quality.pkl")


def air_quality(input_list):
    
    
    res = model.predict(np.asarray(input_list).reshape(1, -1)) 
    # We add '[0]' to the result of the transformed 'res', because 'res' is a list, and we only want 
    # the first element.
    
    if res == 0 or res <= 50 :
        img_string =  "aqi_green"
    elif res >= 50 or res <= 100:
        img_string= "aqi_yellow"
    elif res >= 100 or res <= 150:
        img_string= "aqi_red"
    elif res >= 150 or res <= 200:
        img_string= "aqi_purple"
    elif res >= 200 or res <= 300:
        img_string= "aqi_black"    
        
    passenger_url = "images"  + img_string + ".png"
    img = Image.open(requests.get(passenger_url, stream=True).raw)            
    return img
        
demo = gr.Interface(
    fn=air_quality,
    title="Air Quality Prediction",
    description="Predict the air quality index for a given city and date.",
    allow_flagging="False",
    inputs=[
        gr.inputs.Number(default=1.0, label="Cabin class (1, 2, 3)"),
        gr.Textbox(default='male', label="Sex (male, female)"),
        gr.inputs.Number(default=1.0, label="SibSp (number of siblings/spouses aboard)"),
        gr.inputs.Number(default=1.0, label="Parch (number of parents/children aboard)"),
        gr.Textbox(default="S", label="Port of Embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)"),
        gr.inputs.Number(default=1.0, label="Age"),
        gr.Textbox(default="low", label="Fare_type (low, medium-low, medium, high)"),
        ],
    outputs=gr.Image(type="pil"))

demo.launch(share=True)