import gradio as gr
from PIL import Image
import hopsworks
import datetime 

project = hopsworks.login()
fs = project.get_feature_store()
air_fg = fs.get_or_create_feature_group(name="air_quality_predictions",
                                            version=2,
                                            primary_key=["date"],
                                            description="Air quality predictions"
                                            )

air_fg = air_fg.show(20).sort_values('date', ignore_index=True)
prediction = air_fg.iloc[-1]['pred_aqi']
date = air_fg.iloc[-1]['date']
date_str = datetime.date.fromtimestamp(date//1000).strftime("%Y-%m-%d")
date_tomorrow = air_fg.iloc[-1]["tomorrow_date"]
date_tomorrow_str = datetime.date.fromtimestamp(date_tomorrow//1000).strftime("%Y-%m-%d")



with gr.Blocks() as demo:
    
    if prediction == 0 or prediction <= 50 :
        img_string =  "aqi_green.png"
    elif prediction > 50 or prediction <= 100:
        img_string= "aqi_yellow.png"
    elif prediction > 100 or prediction <= 150:
        img_string= "aqi_red.png"
    elif prediction > 150 or prediction <= 200:
        img_string= "aqi_purple.png"
    else:
        img_string= "aqi_black.png"    
        
    with gr.Row():
      with gr.Column():
          gr.Label(f"Today is {date_str}") 
          gr.Label(f"The Predicted AQI for tomorrow {date_tomorrow_str} in Madrid is {prediction}") 
          input_img = gr.Image("images/" + img_string, elem_id="predicted-img")            

demo.launch()



