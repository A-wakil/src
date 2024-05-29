import cv2
import requests
import base64
import numpy as np
import threading
import queue
import time

# GStreamer pipeline for capturing video from CSI camera
pipeline = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, framerate=30/1 ! "
    "nvvidconv ! video/x-raw, format=BGRx ! "
    "videoconvert ! appsink"
)

def capture_frames(frame_queue):
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: Unable to open camera")
        return

    skip_frame = 2  # Process every 2nd frame
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame")
            break

        if frame_count % skip_frame == 0:
            if not frame_queue.full():
                frame_queue.put(frame)

        frame_count += 1

    cap.release()

def process_frames(frame_queue):
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
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

            except ValueError as e:
                print("Error parsing JSON:", e)
                continue

if __name__ == "__main__":
    frame_queue = queue.Queue(maxsize=10)

    capture_thread = threading.Thread(target=capture_frames, args=(frame_queue,))
    process_thread = threading.Thread(target=process_frames, args=(frame_queue,))

    capture_thread.start()
    process_thread.start()

    try:
        while capture_thread.is_alive() and process_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down...")
        
# add block for logging to be parsed to JSON for writing to csv file, check which option fits best, whethe for ctest, ctest2, of inference.
    
    capture_thread.join()
    process_thread.join()

    cv2.destroyAllWindows()

