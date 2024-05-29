# Import the InferencePipeline object
from inference import InferencePipeline
# Import the built in render_boxes sink for visualizing results
from inference.core.interfaces.stream.sinks import render_boxes

# initialize a pipeline object
pipeline = InferencePipeline.init(
    model_id="primeberrry/3", # Roboflow model to use
    video_reference="rtsp://127.0.0.1:8554/stream", # Path to video, device id (int, usually 0 for built in webcams), or RTSP stream url
    on_prediction=render_boxes, # Function to run after each prediction
)
pipeline.start()
pipeline.join()
