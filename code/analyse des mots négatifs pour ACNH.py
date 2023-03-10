import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from nltk.collocations import QuadgramAssocMeasures, QuadgramCollocationFinder, TrigramAssocMeasures, TrigramCollocationFinder
import plotly.graph_objects as go
import plotly.colors

# Charger le fichier CSV en tant que dataframe
data = pd.read_csv(r"C:\Users\nicol\OneDrive\Nicolas\Bureau\FORMATION\PROJET GAMING SALES\DATAVIZ\AMAZON ET METACRITIC SA VADER NLTK TEXTBLOB.csv")

# Transformer la colonne "date" en datetime
data["date"] = pd.to_datetime(data["date"])

# Filtrer les données pour les examens du titre "ACNH" en mars et avril 2020 avec un score inférieur à 6
filtered_data = data[(data["titre"] == "ACNH") & ((data["date"].dt.year == 2020) & ((data["date"].dt.month == 3) | (data["date"].dt.month == 4))) & (data["score"] < 6)]

# Charger la liste de stopwords en anglais
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Enlever la ponctuation de tous les mots dans les critiques en anglais filtrées avec un score inférieur à 6
all_words = [word.translate(str.maketrans('', '', string.punctuation)) for word in nltk.word_tokenize(" ".join(filtered_data["review_en"].dropna().values.tolist())) if word.lower() not in stop_words and word != '']

# Extraire les 4-grammes les plus fréquents sans espaces
quadgram_measures = QuadgramAssocMeasures()
quadgram_finder = QuadgramCollocationFinder.from_words(all_words)
quadgram_finder.apply_freq_filter(5) # ne garder que les 4-grammes qui apparaissent au moins 5 fois
quadgrams = [tuple(filter(lambda word: ' ' not in word and word.strip(), quadgram)) for quadgram in quadgram_finder.nbest(quadgram_measures.raw_freq, 20)]

# Afficher les 4-grammes les plus fréquents avec leur fréquence
print("Les 20 4-grammes les plus fréquents avec un score inférieur à 6 :")
for quadgram in quadgrams:
    if len(quadgram) == 4:
        print(f"{quadgram[0]} {quadgram[1]} {quadgram[2]} {quadgram[3]} : {quadgram_finder.ngram_fd[quadgram]}")

# Créer un dataframe à partir de la liste des 4-grammes les plus fréquents avec leur fréquence
df = pd.DataFrame([(" ".join(quadgram), quadgram_finder.ngram_fd[quadgram]) for quadgram in quadgrams if len(quadgram) == 4], columns=["4-gramme", "freq"])

# Sauvegarder le dataframe sous forme de fichier CSV
df.to_csv(r"C:\Users\nicol\OneDrive\Nicolas\Bureau\FORMATION\PROJET GAMING SALES\DATASETS FINAUX\N-GRAMMES ACNH.csv", index=False)
"""
# VISUEL

# Créer une liste pour stocker les 4-grammes et leur fréquence
x = []
y = []

# Ajouter les 4-grammes et leur fréquence à la liste
for quadgram in quadgrams:
    if len(quadgram) == 4:
        x.append(f"{quadgram[0]} {quadgram[1]} {quadgram[2]} {quadgram[3]}")
        y.append(quadgram_finder.ngram_fd[quadgram])

# Créer une liste de couleurs pour chaque barre
colors = plotly.colors.qualitative.Plotly

# Créer le graphique
fig = go.Figure(data=[go.Bar(y=x, x=y, orientation='h', marker=dict(color=colors))])

# Inverser l'axe des ordonnées
fig.update_layout(yaxis_autorange="reversed")

# Ajouter un titre centré en grand, gros et gras
fig.update_layout(
    title={
        'text': "Les 10 4-grammes les plus fréquents avec un score inférieur à 6",
        'y':0.98,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=50, color='black', family="Arial, bold")
    }
)

# Modifier la taille des titres des axes
fig.update_layout(
    xaxis_title="Fréquence",
    yaxis_title="4-grammes",
    font=dict(size=40)
)

# Modifier l'apparence des ticks des ordonnées
fig.update_yaxes(tickfont=dict(size=40, color='white'), ticklen=15, tickcolor='white', showgrid=False)
textposition="inside"

# Afficher le graphique
fig.show()
"""