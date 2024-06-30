from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random  # Import random module for exercise selection

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize NLTK resources
nltk.download("vader_lexicon")

# Create sentiment analyzer instance
sia = SentimentIntensityAnalyzer()

# Function to analyze sentiment and detect mood
def analyze_sentiment_and_detect_mood(text):
    sentiment = sia.polarity_scores(text)
    compound_score = sentiment["compound"]

    # Define thresholds for sentiment classification
    if compound_score >= 0.3:
        mood = "positive"
    elif compound_score <= -0.3:
        mood = "negative"
    else:
        mood = "neutral"

    return mood

# Function to suggest exercises based on mood
def suggest_exercises():
    exercises = {
        "positive": [
            "Keep doing activities that make you feel good and energized.",
            "Engage in hobbies or activities that bring you joy and relaxation.",
            "Consider practicing mindfulness or meditation to maintain positivity.",
            "Go for a jog or a brisk walk outdoors.",
            "Try cooking a new healthy recipe.",
            "Listen to uplifting music that boosts your mood.",
            "Write down three things you're grateful for today.",
            "Read an inspiring book or watch a motivational video.",
            "Connect with a friend or loved one over a positive conversation.",
            "Volunteer for a cause you care about."
        ],
        "negative": [
            "Try going for a walk or light exercise to uplift your mood.",
            "Practice deep breathing exercises or yoga to relax your mind and body.",
            "Engage in activities like reading or listening to music that bring comfort.",
            "Write down your thoughts in a journal to release negativity.",
            "Watch a funny movie or show to lift your spirits.",
            "Spend time in nature to recharge and find peace.",
            "Try progressive muscle relaxation techniques.",
            "Reach out to a trusted friend or therapist for support.",
            "Create a calming environment at home with soothing scents and lighting.",
            "Reflect on past challenges and how you overcame them."
        ],
        "neutral": [
            "Take some time for self-reflection and to relax.",
            "Consider trying new activities or hobbies to discover what brings you joy.",
            "Maintain a balanced routine and prioritize self-care.",
            "Create a vision board with your goals and aspirations.",
            "Practice mindful eating and savor each bite.",
            "Explore a nearby park or nature trail.",
            "Attend a local community event or workshop.",
            "Set aside time each day for quiet meditation or prayer.",
            "Take a digital detox and disconnect from screens for a while.",
            "Learn a new skill or take up a creative hobby."
        ]
    }

    # Return a randomly chosen exercise from the appropriate mood list
    mood = session.get("mood", "neutral")  # Default to neutral if mood not set
    return random.choice(exercises.get(mood, exercises["neutral"]))

@app.route("/")
def home():
    # Clear session on homepage reload for testing purposes
    session.clear()
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message").strip().lower()

    # Check if greeted is in session
    if "greeted" not in session or not session["greeted"]:
        session["greeted"] = True
        return jsonify({"response": "Hello!! How are you feeling today?"})

    # Analyze sentiment and detect mood
    mood = analyze_sentiment_and_detect_mood(user_input)
    session["mood"] = mood  # Store mood in session

    # Get a random exercise recommendation based on detected mood
    exercise = suggest_exercises()

    # Format the response to show exercise recommendation on a new line
    response = f"Here's an exercise that might help:\n{exercise}"

    # Return the formatted response
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
