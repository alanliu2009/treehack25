import cv2
import os

FRAMES_FOLDER = "frames"
os.makedirs(FRAMES_FOLDER, exist_ok=True)

def extract_frames(video_path, frame_rate=1):
    cap = cv2.VideoCapture(video_path)
    count = 0
    frame_list = []

    while cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_MSEC, count * 1000)  # Capture every second
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(FRAMES_FOLDER, f"frame_{count}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_list.append(frame_path)
        count += 1

    cap.release()
    print(f"Extracted {count} frames")
    return frame_list
