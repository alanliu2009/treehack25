from flask import Flask, request, jsonify
from downloader import download_zoom_recording
from frame_extractor import extract_frames  # Assuming you have this function for frame extraction
from sentiment import analyze_faces  # Assuming you have this function for sentiment analysis
import threading
import os

app = Flask(__name__)

# Load your Zoom verification token
ZOOM_VERIFICATION_TOKEN = os.getenv("ZOOM_VERIFICATION_TOKEN", "YAA7Hqj3R0WLj5f7oIVnSQ")
RECORDINGS_FOLDER = "recordings"

def process_video(video_path):
    """Process the video after downloading (extract frames, analyze sentiment)."""
    print("Extracting frames from video...")
    frames = extract_frames(video_path)  # Function to extract frames

    print("Analyzing sentiment...")
    avg_sentiment = analyze_faces(frames)  # Function to analyze sentiment

    print(f"Meeting Sentiment Score: {avg_sentiment}")
    if avg_sentiment > 0:
        print("Meeting had a **positive** sentiment 😊")
    elif avg_sentiment < 0:
        print("Meeting had a **negative** sentiment 😞")
    else:
        print("Meeting was **neutral** 😐")

@app.route('/zoom-webhook', methods=['POST'])
def zoom_webhook():
    data = request.json

    print(f"Received Webhook: {data}")

    # Verify the request is from Zoom
    if "token" in data and data["token"] != ZOOM_VERIFICATION_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

    # Respond to Zoom's challenge request (initial verification)
    if data.get("event") == "endpoint.url_validation":
        return jsonify({"plainToken": data["payload"]["plainToken"]})

    # Process recording completion events
    if data.get("event") == "recording.completed":
        recording_files = data['payload']['object']['recording_files']
        download_token = data['download_token']  # Extract the token

        print(f"✅ Download Token: {download_token}")

        for file in recording_files:
            if file['file_extension'].upper() == 'MP4':
                recording_url = file['download_url']
                # Start the download in a separate thread
                threading.Thread(target=download_zoom_recording, args=(recording_url, download_token)).start()
                
                # Once the download completes, process the video
                # Wait for the file to download (you can implement a better check for file existence)
                file_path = os.path.join(RECORDINGS_FOLDER, "meeting.mp4")
                if os.path.exists(file_path):
                    threading.Thread(target=process_video, args=(file_path,)).start()
                break

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
