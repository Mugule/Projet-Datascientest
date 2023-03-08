import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

# Chemin vers le webdriver pour Chrome
DRIVER_PATH = 'C:/chromedriver.exe'

# Liste des URL de la page des évaluations de Zelda Breath of the Wild sur Amazon France
url_templates = [
    "https://www.amazon.fr/Nintendo-NINA66-UK-45ST-Pokemon-Sword/product-reviews/B07DMFDC6W/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={page_num}", 
    "https://www.amazon.fr/Nintendo-Pok%C3%A9mon-Bouclier/product-reviews/B07R2M7H64/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={page_num}", 
]

# Initialisation des listes pour les différentes variables
review_ids = []
contents = []
stars = []
dates = []
urls = []

# Lancement de la navigation automatisée avec Chrome
with webdriver.Chrome(executable_path=DRIVER_PATH) as driver:
    # Accepter les cookies
    driver.get("https://www.amazon.fr")
    try:
        cookie_accept_button = driver.find_element_by_id("sp-cc-accept")
        cookie_accept_button.click()
    except:
        pass

    # Boucle pour parcourir toutes les pages d'avis pour chaque URL
    for url_template in url_templates:
        # Navigation vers la première page des évaluations de Zelda Breath of the Wild
        page_num = 1
        driver.get(url_template.format(page_num=page_num))

        # Boucle pour parcourir toutes les pages d'avis
        while True:
            # Récupération de tous les avis sur la page
            reviews_html = driver.find_elements(By.CSS_SELECTOR, "[data-hook='review']")

            # Si aucun avis n'est trouvé, on arrête la navigation
            if not reviews_html:
                break

            # Parcours des avis et extraction des données
            for review_html in reviews_html:
                # Conversion de l'élément HTML en objet BeautifulSoup pour faciliter l'extraction des données
                review = BeautifulSoup(review_html.get_attribute("innerHTML"), "html.parser")

                # ID de l'avis
                review_id = review_html.get_attribute("id")
                review_ids.append(review_id)

                # Contenu de l'avis
                content = review.find("span", {"data-hook": "review-body"}).get_text(strip=True)
                contents.append(content)

                # Étoiles de l'avis
                star = int(review.find("span", class_="a-icon-alt").get_text(strip=True)[0])
                stars.append(star)

                # Date de l'avis
                date = review.find("span", {"data-hook": "review-date"}).get_text(strip=True)
                dates.append(date)
                
                # URL de l'avis
                url = driver.current_url
                urls.append(url)

            # Clic sur le bouton Suivant pour accéder à la page suivante d'avis
            next_link = driver.find_elements(By.XPATH, "//a[text()='Suivant']")
            if not next_link:
                break
            page_num += 1
            driver.get(url_template.format(page_num=page_num))
            time.sleep(1)

# Création du DataFrame pandas
df = pd.DataFrame({
    "ID": review_ids,
    "Content": contents,
    "Stars": stars,
    "Date": dates,
})

# Enregistrement du DataFrame dans un fichier CSV
df.to_csv("AMAZON SA PKM.csv", index=False)

# Affichage des informations sur le DataFrame
print(df.shape)
print(df.head())
