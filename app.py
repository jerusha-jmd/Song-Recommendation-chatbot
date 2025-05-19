from flask import Flask, render_template, request
import random
from textblob import TextBlob

app = Flask(__name__)

# Mood-based song database
MOOD_SONGS = {
    "happy": ["Happy - Pharrell Williams", "Uptown Funk - Bruno Mars"],
    "sad": ["Someone Like You - Adele", "Hurt - Johnny Cash"],
    "angry": ["Break Stuff - Limp Bizkit", "Killing in the Name - RATM"],
    "calm": ["Weightless - Marconi Union", "Clair de Lune - Debussy"]
}

def detect_mood(text):
    """Analyze text sentiment and return a mood category"""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad" if "sad" in text.lower() else "angry"
    elif polarity > 0:
        return "calm"
    return "neutral"

@app.route('/', methods=['GET', 'POST'])
def mood_recommender():
    song = None
    if request.method == 'POST':
        user_text = request.form.get('user_text', '').strip()
        if user_text:
            mood = detect_mood(user_text)
            song = random.choice(MOOD_SONGS.get(mood, ["Try being more specific!"]))
    
    return render_template('mood.html', song=song)

if __name__ == '__main__':
    app.run(debug=True, port=5000)