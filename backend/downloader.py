import requests
import os
import base64

RECORDINGS_FOLDER = "recordings"
os.makedirs(RECORDINGS_FOLDER, exist_ok=True)

CLIENT_ID = os.getenv("ZOOM_CLIENT_ID", "qoDFAKSxRG3jurjTeW8jw")
CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET", "kNASNuuUGs2xYSEMHYqeYzWgRj3dmm7s")
TOKEN_URL = "https://zoom.us/oauth/token"

def get_zoom_access_token():
    """Fetches a new access token using Client ID & Secret"""
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}  # This will get a new token

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"❌ Failed to get access token: {response.json()}")
        return None

def download_zoom_recording(recording_url, download_token):
    """Downloads the Zoom recording using the provided download token."""
    headers = {"Authorization": f"Bearer {download_token}"}  # ✅ Use the webhook-provided token

    try:
        response = requests.get(recording_url, headers=headers, stream=True)

        # Check if the token has expired (HTTP 401)
        if response.status_code == 401:
            print("❌ Token expired. Refreshing token...")
            new_token = get_zoom_access_token()
            if not new_token:
                print("❌ Failed to refresh token, skipping download.")
                return
            return download_zoom_recording(recording_url, new_token)  # Retry download with new token

        response.raise_for_status()

        file_path = os.path.join(RECORDINGS_FOLDER, "meeting.mp4")
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ Successfully downloaded Zoom recording to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Download failed: {e}")
