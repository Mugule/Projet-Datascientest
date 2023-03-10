# Importer les bibliothèques nécessaires
import pandas as pd
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')



# Charger le fichier CSV
df = pd.read_csv(r"*****AMAZON ET METACRITIC ENG SA.csv")
df['review_en'] = df['review_en'].astype(str)

# Créer une fonction pour l'analyse de sentiment TextBlob
def get_textblob_sentiment(review):
    analysis = TextBlob(review)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# Créer une fonction pour l'analyse de sentiment VADER
def get_vader_sentiment(review):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(review)
    if scores['compound'] > 0:
        return 'positive'
    elif scores['compound'] == 0:
        return 'neutral'
    else:
        return 'negative'

# Créer une fonction pour l'analyse de sentiment NLTK
def get_nltk_sentiment(review):
    nltk_sentiment = nltk.sentiment.SentimentIntensityAnalyzer()
    sentiment_score = nltk_sentiment.polarity_scores(review)
    if sentiment_score['compound'] > 0:
        return 'positive'
    elif sentiment_score['compound'] == 0:
        return 'neutral'
    else:
        return 'negative'

# Ajouter les colonnes de sentiment au dataframe
df['sentiment TEXTBLOB'] = df['review_en'].apply(get_textblob_sentiment)
df['sentiment VADER'] = df['review_en'].apply(get_vader_sentiment)
df['sentiment NLTK'] = df['review_en'].apply(get_nltk_sentiment)

# Sauvegarder le dataframe dans un nouveau fichier CSV
df.to_csv(r"****AMAZON ET METACRITIC SA VADER NLTK TEXTBLOB.csv", index=False)

print(df.head(100))
