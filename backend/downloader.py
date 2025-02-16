import requests
import os

RECORDINGS_FOLDER = "recordings"
os.makedirs(RECORDINGS_FOLDER, exist_ok=True)

# def download_zoom_recording(url):
#     filename = os.path.join(RECORDINGS_FOLDER, "meeting.mp4")
    
#     response = requests.get(url, stream=True)
#     with open(filename, "wb") as f:
#         for chunk in response.iter_content(chunk_size=1024):
#             f.write(chunk)
    
#     print(f"Downloaded Zoom recording to {filename}")
#     return filename

def download_zoom_recording(recording_url):
    try:
        response = requests.get(recording_url, stream=True)
        response.raise_for_status()

        file_path = os.path.join(RECORDINGS_FOLDER, "meeting.mp4")
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ Successfully downloaded Zoom recording to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Download failed: {e}")