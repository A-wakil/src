# capture_and_send.py
import cv2
import requests
import base64
import numpy as np

# GStreamer pipeline for capturing video from CSI camera
pipeline = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, framerate=30/1 ! "
    "nvvidconv ! video/x-raw, format=BGRx ! "
    "videoconvert ! appsink"
)

cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Unable to open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame")
        break

    # Convert frame to base64 string
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')

    # Send the image to the inference server
    response = requests.post(
        "http://10.1.12.47:5000/infer",
        json={"image": jpg_as_text}
    )

    # Print the raw response for debugging
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        result = response.json()
        print("Parsed JSON:", result)
    except ValueError as e:
        print("Error parsing JSON:", e)
        continue

    # Process the response
    if 'predictions' in result:
        for prediction in result['predictions']:
            x0 = int(prediction['x'] - prediction['width'] / 2)
            y0 = int(prediction['y'] - prediction['height'] / 2)
            x1 = int(prediction['x'] + prediction['width'] / 2)
            y1 = int(prediction['y'] + prediction['height'] / 2)
            label = prediction['class']

            # Draw rectangle
            cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
            # Draw label
            cv2.putText(frame, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("CSI Camera - Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

