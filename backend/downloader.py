import requests
import os

RECORDINGS_FOLDER = "recordings"
os.makedirs(RECORDINGS_FOLDER, exist_ok=True)

def download_zoom_recording(url):
    filename = os.path.join(RECORDINGS_FOLDER, "meeting.mp4")
    
    response = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
    
    print(f"Downloaded Zoom recording to {filename}")
    return filename