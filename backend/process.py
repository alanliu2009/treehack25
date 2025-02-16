from downloader import download_zoom_recording
from frame_extractor import extract_frames
from sentiment import analyze_faces
import os

def process_video(video_path):
    print("Extracting frames from video...")
    frames = extract_frames(video_path)

    print("Analyzing sentiment...")
    avg_sentiment = analyze_faces(frames)

    print(f"Meeting Sentiment Score: {avg_sentiment}")
    if avg_sentiment > 0:
        print("Meeting had a **positive** sentiment 😊")
    elif avg_sentiment < 0:
        print("Meeting had a **negative** sentiment 😞")
    else:
        print("Meeting was **neutral** 😐")

if __name__ == "__main__":
    video_file = os.path.join("recordings", "meeting.mp4")
    print("video file: " + video_file)
    if os.path.exists(video_file):
        process_video(video_file)
    else:
        print("No recording found!")
