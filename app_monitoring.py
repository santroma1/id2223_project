import gradio as gr
from PIL import Image
import hopsworks

project = hopsworks.login()
fs = project.get_feature_store()

dataset_api = project.get_dataset_api()


with gr.Blocks() as demo:
    with gr.Row():
      with gr.Column():
          gr.Label("Today's Predicted Image")
          input_img = gr.Image("images/aqi_green.png", elem_id="predicted-img")
      with gr.Column():          
          gr.Label("Today's Actual Image")
          input_img = gr.Image("images/aqi_green.png", elem_id="actual-img")        
    # with gr.Row():
    #   with gr.Column():
    #       gr.Label("Recent Prediction History")
    #       input_img = gr.Image("df_recent.png", elem_id="recent-predictions")        

demo.launch()



