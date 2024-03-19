import os.path
import numpy as np
import cv2
from os.path import join
import matplotlib.pyplot as plt


def crop_video(input_path, start_frame, end_frame, x_start, x_end, y_start, y_end):
    # Load the video
    cap = cv2.VideoCapture(join(input_path, 'video.mp4'))

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = x_end - x_start
    height = y_end - y_start
    outname = f'cropped_{start_frame}_{end_frame}_{x_start}_{x_end}_{y_start}_{y_end}'
    output_path = join(input_path, f'{outname}.mp4')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # If the current frame is within the start and end frames, crop and write it
        if start_frame <= frame_count <= end_frame:
            cropped_frame = frame[y_start:y_end, x_start:x_end]
            out.write(cropped_frame)

        frame_count += 1

    # Release everything
    cap.release()
    out.release()

    timestamps = np.load(os.path.join(input_path, 'timestamps.npy'))

    timestamps = timestamps[start_frame:end_frame]
    np.save(os.path.join(input_path, f'{outname}.npy'), timestamps)

def show_frame(video_path, frame_number):
    # Load the video
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # If the current frame is the 5th frame, display it
        if frame_count == frame_number:
            plt.imshow(frame)
            print(frame.shape)
            plt.show()
            break

        frame_count += 1

    # Release the video
    cap.release()



datadir = 'data/input/joris'
crop = True
# Usage

if crop:
    crop_video(datadir, start_frame=100, end_frame=300, x_start=300, x_end=1500, y_start=50, y_end=1080)
else:
    show_frame(join(datadir, 'video.mp4'), frame_number=200)