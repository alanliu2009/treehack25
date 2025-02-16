# ZoomPulse

### TreeHacks 2025 by Maggie Liu, Julia Ding, and Alan Liu

## Setup

- Install ngrok and run `ngrok http 5000` in your terminal to retrieve a target URL, and use it as the web target on Zoom App Marketplace.
- Run `pip install -r requirements.txt` in both the frontend and backend directories.

## Running the Program

1. Start by enabling the frontend development server by running 'npm start'.
2. Enable the backend webhook with 'python3 app.py'.
3. Now, record a Zoom call to the cloud, and your call will automatically retrieved by the webhook.
4. Check the webpage to get a review of the video sentiment!
