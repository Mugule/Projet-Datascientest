from requests_html import HTMLSession
import pandas as pd

# initialiser une session HTML
sess = HTMLSession()

# fonction pour extraire les commentaires
def get_reviews(url):
    reviews_list = []  # initialiser la liste des commentaires
    res = sess.get(url)  # envoyer une requête GET à l'URL donnée
    html = res.html  # récupérer le contenu HTML de la page
    reviews = html.find('.product_reviews', first=True).find('[class="review_section"]')  # extraire tous les éléments HTML qui contiennent les commentaires
    for review in reviews:
        try:
            review_body = review.find('.blurb_expanded', first=True).text  # extraire le texte du commentaire
        except AttributeError:
            review_body = review.find('.review_body', first=True).text  # si le commentaire est trop court, extraire le texte de la section "review_body" à la place
        reviews_list.append({
              'author': review.find('.name', first=True).text  # extraire le nom de l'auteur
            , 'review': review_body  # ajouter le texte du commentaire
            , 'date': review.find('.date', first=True).text  # extraire la date du commentaire
            , 'score': int(review.find('.review_grade', first=True).text)  # extraire la note attribuée au commentaire et la convertir en entier
            })
    next_page = html.find('.flipper.next', first=True)  # chercher le bouton "next"
    if next_page:
        try:
            next_page_url = next_page.absolute_links.pop()  # extraire l'URL de la page suivante
            reviews_list[-1]['next_page_url'] = next_page_url  # ajouter l'URL de la page suivante à la dernière revue de la liste
            reviews_list.extend(get_reviews(next_page_url))  # extraire les commentaires de la page suivante et les ajouter à la liste
        except KeyError:
            pass
    return reviews_list

# URL de la page de commentaires
url = 'https://www.metacritic.com/game/switch/the-legend-of-zelda-breath-of-the-wild/user-reviews'

# extraire les commentaires de toutes les pages
all_reviews = get_reviews(url)
while all_reviews[-1].get('next_page_url'):  # tant qu'il y a une page suivante
    url = all_reviews[-1]['next_page_url']  # extraire l'URL de la page suivante
    all_reviews.extend(get_reviews(url))  # extraire les commentaires de la page suivante et les ajouter à la liste

# créer un dataframe pandas à partir des commentaires
df = pd.DataFrame(all_reviews, columns=['author', 'date', 'review', 'score'])

# enregistrer le dataframe au format CSV
df.to_csv('SA METACRITIC BOTW.csv', index=False, encoding='utf-8')

# afficher les 5 premières lignes du dataframe
print(df.head())
print(df.shape)