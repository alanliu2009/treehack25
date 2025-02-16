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
latest_video_path = None
# latest_sentiment_score = None

@app.route('/process_video', methods=['GET'])
def process_video():
    # global latest_sentiment_score, latest_video_path
    global latest_video_path

    if not latest_video_path or not os.path.exists(latest_video_path):
        print("No video found for processing.")
        return
    """Process the video after downloading (extract frames, analyze sentiment)."""
    print("Extracting frames from video...")
    frames = extract_frames(latest_video_path)  # Function to extract frames

    print("Analyzing sentiment...")
    avg_sentiment = analyze_faces(frames)  # Function to analyze sentiment

    print(f"Meeting Sentiment Score: {avg_sentiment}")
    if avg_sentiment > 0:
        print("Meeting had a **positive** sentiment 😊")
    elif avg_sentiment < 0:
        print("Meeting had a **negative** sentiment 😞")
    else:
        print("Meeting was **neutral** 😐")
    ret_sent = 50 * (avg_sentiment + 1)
    print(ret_sent)
    return str(ret_sent)

@app.route('/zoom-webhook', methods=['POST'])
def zoom_webhook():
    global latest_video_path
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
                    latest_video_path = file_path
                    threading.Thread(target=process_video).start()
                break

    return jsonify({"status": "received"}), 200

# @app.route('/process_video', methods=['GET'])
# def process_video_endpoint():
#     """Trigger video processing and return the result."""
#     threading.Thread(target=process_video).start()
#     return jsonify({"message": "Processing started"})


# @app.route('/video_status', methods=['GET'])
# def video_status():
#     """Check if the video processing is done and return the score."""
#     if latest_sentiment_score is None:
#         return jsonify({"status": "processing"}), 202
#     return jsonify({"status": "done", "sentiment_score": latest_sentiment_score})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
