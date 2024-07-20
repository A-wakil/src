from flask import Flask, request, jsonify
from roboflow import Roboflow
import base64
import cv2
import numpy as np
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initializing Roboflow model
rf = Roboflow(api_key="F5PelvcDYgrcgAuDsRtE")
project = rf.workspace("primeberry").project("asabe-kqx8j")
model = project.version("2").model

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

        # Performing inference on the image/frame
        result = model.predict(img, confidence=50, overlap=30).json()
        logging.debug("Inference result: %s", result)

        # Excluding non-serializable fields from the response
        serializable_result = {
            "predictions": [
                {key: value for key, value in prediction.items() if key != "image_path"}
                for prediction in result["predictions"]
            ],
            "image": result.get("image", {})
        }

        return jsonify(serializable_result)
    except Exception as e:
        logging.error("Error during inference: %s", e)
        return jsonify({"error": str(e)}), 500

@app.route('/infer_batch', methods=['POST'])
def infer_batch():
    try:
        data = request.json
        images = data.get('images', [])
        results = []

        for image_data in images:
            logging.debug("Received image data length: %d", len(image_data))
            
            # Decode base64 string to image
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("Failed to decode image")
            
            logging.debug("Image shape: %s", img.shape)

            # Performing inference on the image/frame
            result = model.predict(img, confidence=50, overlap=30).json()
            logging.debug("Inference result: %s", result)

            # Excluding non-serializable fields from the response
            serializable_result = {
                "predictions": [
                    {key: value for key, value in prediction.items() if key != "image_path"}
                    for prediction in result["predictions"]
                ],
                "image": base64.b64encode(cv2.imencode('.jpg', img)[1]).decode('utf-8')  # Return the processed image
            }

            results.append(serializable_result)

        return jsonify(results)
    except Exception as e:
        logging.error("Error during batch inference: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
