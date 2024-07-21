from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np
import torch
from ultralytics import YOLO
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load the YOLOv8 model
model = YOLO("best.pt")

@app.route('/infer', methods=['POST'])
def infer():
    try:
        data = request.json
        logging.debug("Received request data: %s", data)
        
        image_data = data['image']
        logging.debug("Image data length: %d", len(image_data))
        
        # Decode base64 string to image
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Failed to decode image")
        
        logging.debug("Image shape: %s", img.shape)

        # Perform inference on the image
        results = model(img)

        predictions = []
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                if len(box) < 4:
                    continue
                x0, y0, x1, y1 = box[:4]
                prediction = {
                    "class": int(box[5]),
                    "confidence": float(box[4]),
                    "x": x0 + (x1 - x0) / 2,
                    "y": y0 + (y1 - y0) / 2,
                    "width": x1 - x0,
                    "height": y1 - y0
                }
                predictions.append(prediction)

        # Prepare the results in the required format
        serializable_result = {
            "predictions": predictions,
            "image": {}
        }

        return jsonify(serializable_result)
    except Exception as e:
        logging.error("Error during inference: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
