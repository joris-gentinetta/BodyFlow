import os

import cv2
import time
import threading
import numpy as np
from os.path import join
import signal
import sys

stop_video = False
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    global stop_video
    stop_video = True

    # sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def capture_video(output_dir='testing'):
    global stop_video
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open camera.")
        return

    # Dynamically obtain frame size
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(join(output_dir, 'video.mp4'), fourcc, 24.0, (frame_width, frame_height))
    timestamps = []
    new_time = time.time()
    while True:
        timestamps.append(time.perf_counter())
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab a frame.")
            break

        out.write(frame)
        old_time = new_time
        new_time = time.time()
        print(f"FPS: {1/(new_time-old_time)}")
        print(f"time: {new_time-old_time}")
        # cv2.imshow('frame', frame)


        if stop_video:
            break

    cap.release()
    out.release()
    timestamps = np.array([timing - timestamps[0] for timing in timestamps])
    np.save(join(output_dir, 'timestamps.npy'), timestamps)

    cv2.destroyAllWindows()

datadir = 'data/input/megan'
os.makedirs(datadir, exist_ok=True)
video_thread = threading.Thread(target=capture_video, args=(datadir,))
video_thread.start()
# wait for thread to finish:
video_thread.join()

timestamps = np.load(join(datadir, 'timestamps.npy'))

# Open the video file
cap = cv2.VideoCapture(join(datadir, 'video.mp4'))
# get the frame rate
fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Frame Rate: {fps}")
# get length of the video
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Length: {length}")
print(f'timestamps: {timestamps}')
print(f'len(timestamps): {len(timestamps)}')

