from flask import Flask, request, jsonify
from downloader import download_zoom_recording
import threading
import os

app = Flask(__name__)

# Load your Zoom verification token
ZOOM_VERIFICATION_TOKEN = os.getenv("ZOOM_VERIFICATION_TOKEN", "ODMIR2E2TrCWcR705px6pg")

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

        print(f"Download Token: {download_token}")

        for file in recording_files:
            if file['file_extension'].upper() == 'MP4':
                recording_url = file['download_url']
                # Append token to URL
                recording_url = f"{recording_url}?access_token={download_token}"
                threading.Thread(target=download_zoom_recording, args=(recording_url,)).start()
                break

    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
