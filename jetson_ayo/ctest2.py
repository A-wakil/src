import cv2
import base64
import numpy as np
import threading
import queue
import aiohttp
import asyncio

pipeline = (
    "nvarguscamerasrc ! "
    "video/x-raw(memory:NVMM), width=1280, height=720, framerate=30/1 ! "
    "nvvidconv ! video/x-raw, format=BGRx ! "
    "videoconvert ! appsink"
)

async def send_frames_batch_async(frames_batch):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://10.1.12.26:5000/infer_batch", json={"images": frames_batch}) as response:
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
                # Resize frame before adding to queue
                frame = cv2.resize(frame, (640, 360))
                frame_queue.put(frame)

        frame_count += 1

    cap.release()

async def process_frames(frame_queue):
    batch = []
    batch_size = 5

    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            batch.append(jpg_as_text)

            if len(batch) >= batch_size:
                try:
                    result = await send_frames_batch_async(batch)
                    # Process the results as needed
                    for res in result:
                        if 'predictions' in res:
                            frame = cv2.imdecode(np.frombuffer(base64.b64decode(res['image']), np.uint8), cv2.IMREAD_COLOR)
                            for prediction in res['predictions']:
                                x0 = int(prediction['x'] - prediction['width'] / 2)
                                y0 = int(prediction['y'] - prediction['height'] / 2)
                                x1 = int(prediction['x'] + prediction['width'] / 2)
                                y1 = int(prediction['y'] + prediction['height'] / 2)
                                label = prediction['class']

                                cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
                                cv2.putText(frame, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                            cv2.imshow("CSI Camera - Object Detection", frame)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break

                except Exception as e:
                    print("Error processing batch:", e)
                finally:
                    batch = []  # Clear batch after processing

        # Handle final batch processing if queue is empty
        if len(batch) > 0 and frame_queue.empty():
            try:
                result = await send_frames_batch_async(batch)
                for res in result:
                    if 'predictions' in res:
                        frame = cv2.imdecode(np.frombuffer(base64.b64decode(res['image']), np.uint8), cv2.IMREAD_COLOR)
                        for prediction in res['predictions']:
                            x0 = int(prediction['x'] - prediction['width'] / 2)
                            y0 = int(prediction['y'] - prediction['height'] / 2)
                            x1 = int(prediction['x'] + prediction['width'] / 2)
                            y1 = int(prediction['y'] + prediction['height'] / 2)
                            label = prediction['class']

                            cv2.rectangle(frame, (x0, y0), (x1, y1), (0, 255, 0), 2)
                            cv2.putText(frame, label, (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                        cv2.imshow("CSI Camera - Object Detection", frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

            except Exception as e:
                print("Error processing final batch:", e)

if __name__ == "__main__":
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
