from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Set your Zoom verification token
ZOOM_VERIFICATION_TOKEN = os.getenv("ZOOM_VERIFICATION_TOKEN", "your_zoom_token_here")

@app.route("/zoom-webhook", methods=["POST"])
def zoom_webhook():
    data = request.json
    
    # Handle endpoint validation
    if data.get("event") == "endpoint.url_validation":
        return jsonify({
            "plainToken": data["payload"]["plainToken"]
        })
    
    # Validate Zoom verification token
    if data.get("token") != ZOOM_VERIFICATION_TOKEN:
        return jsonify({"message": "Unauthorized"}), 401
    
    # Print the incoming payload
    print("Received Zoom Webhook:", data)
    
    return jsonify({"message": "Webhook received successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)