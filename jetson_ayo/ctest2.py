import cv2
import requests
import base64
import numpy as np
import threading
import queue
import time
import aiohttp
import asyncio
import csv

pipeline = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, framerate=30/1 ! "
    "nvvidconv ! video/x-raw, format=BGRx ! "
    "videoconvert ! appsink"
)

# Initialize CSV file
csv_file = 'detection_results.csv'
fieldnames = ['timestamp', 'class', 'count']

# Define all possible classes
all_classes = ['healthy', 'flowers', 'unhealthy']  # Replace with your actual class names

def init_csv():
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

async def send_frame_async(jpg_as_text):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://10.1.12.26:5000/infer", json={"image": jpg_as_text}) as response:
            result = await response.json()
            return result

def capture_frames(frame_queue):
    cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Error: Unable to open camera")
        return

    skip_frame = 2
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

async def process_frames(frame_queue):
    detection_counts = {cls: 0 for cls in all_classes}
    start_time = time.time()

    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            try:
                result = await send_frame_async(jpg_as_text)
                print("Parsed JSON:", result)

                if 'predictions' in result:
                    # Reset counts for each detection cycle
                    current_counts = {cls: 0 for cls in all_classes}

                    for prediction in result['predictions']:
                        label = prediction['class']
                        if label in current_counts:
                            current_counts[label] += 1

                        x0 = int(prediction['x'] - prediction['width'] / 2)
                        y0 = int(prediction['y'] - prediction['height'] / 2)
                        x1 = int(prediction['x'] + prediction['width'] / 2)
                        y1 = int(prediction['y'] + prediction['height'] / 2)

                        cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    # Update detection_counts with current_counts
                    detection_counts.update(current_counts)

                cv2.imshow("CSI Camera - Object Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                # Check if 15 seconds have passed
                current_time = time.time()
                if current_time - start_time >= 15:
                    start_time = current_time
                    record_to_csv(detection_counts)

            except Exception as e:
                print("Error processing frame:", e)
                continue

def record_to_csv(detection_counts):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(csv_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for label in all_classes:
            count = detection_counts.get(label, 0)
            writer.writerow({'timestamp': timestamp, 'class': label, 'count': count})

if __name__ == "__main__":
    init_csv()  # Initialize the CSV file

    frame_queue = queue.Queue(maxsize=10)

    capture_thread = threading.Thread(target=capture_frames, args=(frame_queue,))
    capture_thread.start()

    loop = asyncio.get_event_loop()
    process_task = loop.create_task(process_frames(frame_queue))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down...")

    capture_thread.join()
    cv2.destroyAllWindows()
