<<<<<<< HEAD
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(text):
    if not text: return "Neutral", 0
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)
    if score['compound'] >= 0.05:
        return "Positive", score['compound']
    elif score['compound'] <= -0.05:
        return "Negative", score['compound']
    else:
=======
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(text):
    if not text: return "Neutral", 0
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(text)
    if score['compound'] >= 0.05:
        return "Positive", score['compound']
    elif score['compound'] <= -0.05:
        return "Negative", score['compound']
    else:
>>>>>>> fac0a472dd65abb6c62d32d6332a1cdbe873dcc4
        return "Neutral", score['compound']