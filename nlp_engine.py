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
        return "Neutral", score['compound']