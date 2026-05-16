from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# DATABASE SETUP
conn = sqlite3.connect("mindcare.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    sentiment TEXT
)
""")

conn.commit()

# -----------------------------------
# EMOTION DETECTION
# -----------------------------------

def detect_emotion(text):

    analysis = TextBlob(text)

    polarity = analysis.sentiment.polarity

    if polarity > 0.3:
        return "Happy"

    elif polarity < -0.3:
        return "Sad"

    else:
        return "Neutral"


# -----------------------------------
# AI WELLNESS RESPONSE SYSTEM
# -----------------------------------

def generate_response(emotion, text):

    text = text.lower()

    # HAPPY
    if emotion == "Happy":

        return (
            "I'm really happy to hear that 😊 "
            "Keep enjoying the positive moments in your life. "
            "Would you like to share what made your day good?"
        )

    # SAD
    elif emotion == "Sad":

        return (
            "I'm here with you 💜 "
            "It's completely okay to feel sad sometimes. "
            "Please remember that difficult moments will pass. "
            "Try taking a small break, listening to calming music, "
            "or talking to someone you trust."
        )

    # NEUTRAL
    elif emotion == "Neutral":

        # STRESS
        if "stress" in text or "stressed" in text:

            return (
                "It sounds like you're feeling stressed 🌸 "
                "Take a few deep breaths and focus on one thing at a time."
            )

        # TIRED
        elif "tired" in text or "exhausted" in text:

            return (
                "You seem mentally tired 🌿 "
                "Please take some rest and relax for a while."
            )

        # EXAMS
        elif "exam" in text or "study" in text:

            return (
                "Exams can feel overwhelming 📚 "
                "Take short breaks while studying and stay hydrated."
            )

        # LONELY
        elif "alone" in text or "lonely" in text:

            return (
                "You are not alone 💙 "
                "Your feelings matter and support is always available."
            )

        # ANXIETY
        elif "anxiety" in text or "anxious" in text:

            return (
                "I'm sorry you're feeling anxious 🌸 "
                "Try slow breathing and grounding exercises."
            )

        # DEFAULT
        else:

            return (
                "Thank you for sharing your feelings 🌿 "
                "I'm always here to listen."
            )

    # FALLBACK
    else:

        return (
            "Please take care of yourself 🌸 "
            "Your feelings matter."
        )


# -----------------------------------
# HOME ROUTE
# -----------------------------------

@app.route("/")

def home():

    return jsonify({
        "message": "MindCare AI Backend Running Successfully 🚀"
    })


# -----------------------------------
# CHAT API
# -----------------------------------

@app.route("/chat", methods=["POST"])

def chat():

    data = request.get_json()

    user_message = data.get("message")

    emotion = detect_emotion(user_message)

    response = generate_response(emotion, user_message)

    # STORE IN DATABASE
    cursor.execute(
        "INSERT INTO moods (message, sentiment) VALUES (?, ?)",
        (user_message, emotion)
    )

    conn.commit()

    return jsonify({
        "emotion": emotion,
        "response": response
    })


# -----------------------------------
# HISTORY API
# -----------------------------------

@app.route("/history", methods=["GET"])

def history():

    cursor.execute(
        "SELECT message, sentiment FROM moods"
    )

    rows = cursor.fetchall()

    history_data = []

    for row in rows:

        history_data.append({
            "message": row[0],
            "emotion": row[1]
        })

    return jsonify(history_data)


# -----------------------------------
# VERCEL SUPPORT
# -----------------------------------

if __name__ == "__main__":
    app.run(debug=True)
