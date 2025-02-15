from deepface import DeepFace

sentiment_mapping = {
    "happy": 1, "neutral": 0, "surprise": 0.5,
    "sad": -1, "angry": -1, "fear": -0.5, "disgust": -1
}

def analyze_faces(frame_list):
    scores = []
    for frame in frame_list:
        try:
            result = DeepFace.analyze(frame, actions=['emotion'])
            emotion = result[0]['dominant_emotion']
            scores.append(sentiment_mapping.get(emotion, 0))  # Default to neutral
        except:
            scores.append(0)  # Assume neutral if no face is detected
    
    avg_sentiment = sum(scores) / len(scores) if scores else 0
    return avg_sentiment
