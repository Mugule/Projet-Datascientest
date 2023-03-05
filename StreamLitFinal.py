
# %% (_.~" IMPORT "~._) 

import datetime
import numpy as np
import pandas as pd

from PIL import Image

import streamlit as st
from streamlit_option_menu import option_menu

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly import tools

loremIpsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue. Praesent egestas leo in pede. Praesent blandit odio eu enim. Pellentesque sed dui ut augue blandit sodales. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam nibh. Mauris ac mauris sed pede pellentesque fermentum. Maecenas adipiscing ante non diam sodales hendrerit. '


# %% (_.~" METHODES "~._) 

def weighted_average(group):
        weights_sum = np.sum(group[qty])
        if weights_sum > 0:
            return np.average(group[qly], weights=group[qty])
        else:
            return np.nan

# %% (_.~" DATAFRAMES "~._)  
# %%% Import
# DataFrame principal
df = pd.read_csv("finalDataset.csv")
# Dataframe de base venant de VGChartz
dfVGSales = pd.read_csv("vgsales.csv", index_col=[0]) 
# %%% Formatage df
# Création de la colonne Date
df["Date"] = pd.to_datetime(df['Year'].astype("str")+" "+df['Month'].astype("str"),format="%Y %m")
# Réparation coquilles
df = df.replace("SSMU", "SSBU")
df = df[df["Date"]<='2023-01-01']


# %%% Céation de dfmean
# Instances
CountList = ['countMTC','countAMZ']
MeanList = ['meanMTC','meanAMZ']
dfNoNan = df
dfmean = pd.DataFrame()
dfcount = pd.DataFrame()
# Calcul de la moyenne pondérée pour chaque groupe
for qty, qly in zip(CountList,MeanList):
    dfNoNan[qty] = dfNoNan[qty].fillna(0)
    dfNoNan[qly] = dfNoNan[qly].fillna(0)
    dfmean = dfmean.append(dfNoNan.groupby("Game").apply(weighted_average),ignore_index=True)
# Mise en forme du dataframe
dfmean = dfmean.rename(index=dict(zip(dfmean.index, MeanList)))
dfmean = dfmean.T.reset_index()
dfmean = pd.concat([dfmean,
                    dfNoNan.groupby("Game").agg({'countAMZ':"sum"}).reset_index(drop=True),
                    dfNoNan.groupby("Game").agg({"countMTC":"sum"}).reset_index(drop=True)], 
                    axis=1)
# Suppression de SWCH et TOTL
dfmean = dfmean.drop([5,6])

# %%% ColorDict
colorDict = {}

for name in dfVGSales.Publisher.unique():
    if name == 'Nintendo':
        colorDict[name] = "red"
    elif name == 'Electronic Arts':
        colorDict[name] = "blue"
    elif name == 'Activision':
        colorDict[name] = "cornflowerblue"
    else:
        colorDict[name] = "grey"

# %% (_.~" STREAMLIT "~._) 

# %%% Navigation

st.set_page_config(page_title="Switch Bestsellers",
                   page_icon=":video_game:")

with st.sidebar:
    selectedMenu = option_menu(
        menu_title = "Switch bestsellers",
        menu_icon= "nintendo-switch",
        options = ["Projet",
                   "Contexte",
                   "Methodologie",
                   "Analyses",
                   "Conclusion",
                   "Scrap-App"],
        icons = ["easel",
                 "info",
                 "cloud-download",
                 "graph-up",
                 "controller",
                 "twitter"])

# %%% Projet

if selectedMenu == "Projet":
    
    
    # Image
    st.image("medias/imgpresentation.png")
    
    st.markdown("<h4 style='text-align: center;'>Peut-on utiliser Twitter comme facteur prédictif des ventes?</h3>", unsafe_allow_html=True)
    
    st.markdown("Pour ce projet, nous avons choisi l’analyse des ventes de jeux vidéo sur l’axe du storytelling. Nous le ferons via du scrapping, du text mining puis un sentiment analysis sur le dataset obtenu. Le projet sera dans une démarche de rétrospection plutôt que de prédiction. L’idée est de mieux comprendre ce qu’il s’est passé pour préparer de futures campagnes marketing (par exemple).")
    
    st.markdown("Projet présenté par")
    col1, col2, col3 = st.columns(3)

    with col1:
       st.subheader("Michael Deroche")
    
    with col2:
       st.subheader("Nicolas Brown")
    
    with col3:
       st.subheader("Julien Petit")
    
    st.caption('_ - Promotion JAN 2023 Datascientest - _') 

# %%% Contexte

if selectedMenu == "Contexte":
    
    st.title("Contexte")
    
    # %%%% Introduction
    
    st.header("Les premières données")
    
    # imageVGChartz
    imageVGChartz = "https://www.vgchartz.com/assets/images/vgchartz-logo-horizontal.png"
    st.image(imageVGChartz)
    
    st.markdown("Les données fournies par DataScientest viennent d'un scrapping réalisé sur le site VGChartz par 'GregorySmith' disponible sur le site Kaggle ([ou ici](https://www.kaggle.com/datasets/gregorut/videogamesales)). Après une première visualisation des données, nous verrons pourquoi nous avons décidé d'obtenir nos propres données pour réaliser une analyse. Vous trouverez ci-dessous les données brutes et notre première exploration de données.")
              
    st.dataframe(dfVGSales.head(5))

    st.markdown("Les chiffres des ventes parcours la grandes partis des jeux allant de 1980 à 2016 (4 jeux au delà de cette période). Cela s'éxplique par un changement de méthodologie du site VGChartz expliqué [ici](https://www.vgchartz.com/methodology.php).") 

    st.markdown("Wii Sports la vente numéro 1 se détache complètement du reste. Cette valeur aberrante s'explique facilement car ce jeu a été vendu systématiquement avec chaque Nintendo Wii (à part au Japon et en Corée du Sud). On ne peut pas vraiment parler d'un choix du consommateur mais plus d'un jeu 'gratuit'. On peut quand même mesurer le succès du jeu grâce à sa deuxième version : Wii Sports Resort. Afin de ne pas fausser les graphiques, nous supprimerons la ligne concernant Wii Sports.")

    st.markdown("Enfin, on peut noter 278 valeurs manquantes pour les années et 58 pour les éditeurs. Nous verrons plus tard que nous allons créer de toute pièce nos dataset via scrapping, il n’est donc pas nécessaire de s’attarder sur celle-ci.")
    
    # %%%% Première Exploration
    
    st.subheader('Exploration du Dataset')
    
    st.markdown("Après analyse, nous avons pu voir que Nintendo sort des jeux extrêmement qualitatifs. En effet, si on le compare avec Activision et EA (Electronic Arts) qui sont des mastodontes, nous allons voir que les chiffres de ventes ne suit pas de la même manière. Sur ces deux premiers graphiques. Nous allons voir le nombre de titres uniques vendus par éditeur en comparaison avec le nombre total des ventes (en millions de dollars).")

    
    bestPublisherSales = dfVGSales[dfVGSales["Publisher"].isin(dfVGSales["Publisher"] \
                                                     .value_counts()[0:10].index)] \
                                                     .groupby(["Publisher"]) \
                                                     .agg({"Global_Sales":"sum"}) \
                                                     .reset_index(level='Publisher') \
                                                     .sort_values(by=["Global_Sales"], ascending=False)

    bestPublisherUnits = pd.DataFrame(dfVGSales.Publisher.value_counts()[0:10].sort_values()).reset_index() \
                                                                                             .rename(columns={"index": 'Publisher', 'Publisher': "Titles"}) \
                                                                                            .sort_values(by=["Titles"], ascending=False)
    
    # Suppression de WiiSport
    dfVGSales = dfVGSales.drop([1])
    
    # Graph Titre par éditeur

    vgPublUnit = px.bar(bestPublisherUnits, 
                 x="Titles", 
                 y="Publisher",
                 color="Publisher",
                 color_discrete_map = colorDict,
                 labels={"Publisher": "Editeurs",
                         "Titles": "Total des titres sortis"},
                 title="Nombre de titres uniques sortis par éditeurs",
                 text_auto='.2s',
                 orientation='h')
    
    st.plotly_chart(vgPublUnit)
    
    # Graph Ventes par éditeur
    
    vgPublSals = px.bar(bestPublisherSales, 
                        x="Global_Sales", 
                        y="Publisher",
                        color="Publisher",
                        color_discrete_map = colorDict,
                        labels={"Publisher": "Editeurs",
                                "Global_Sales": "Total des ventes mondiales (M$)"},
                        title="Ventes par éditeur",
                        text_auto='.2s',
                        orientation='h')
    
    st.plotly_chart(vgPublSals)

    st.markdown("Si dans le premier cas Nintendo n’est pas en tête avec seulement 700 titres sortis contre 1400 titres chez EA (soit le double), on remarque que les ventes totales sont à 1700M chez Nintendo ! Si EA tient la deuxième position avec 1100M on voit que certains comme Namco Bandai peinent à réaliser le même résultat avec un peu plus de 250M . Nintendo atteint un peu plus de 2.4M par titre. Dans les plus gros éditeurs, c’est tout simplement énorme. Alors même si les autres éditeurs s’en tirent bien du point de vue commercial, Nintendo domine-t-il par des bestsellers sur différentes années?")

    # Graph meilleurs titres
    
    vgBestTitl_df = dfVGSales.groupby(['Year','Publisher','Name']).agg({"Global_Sales":"sum"}).reset_index(level=['Year','Publisher','Name'])
    vgBestTitl_cond = vgBestTitl_df.groupby('Year')['Global_Sales'].transform('max') == vgBestTitl_df['Global_Sales']
    vgBestTitl = px.bar(vgBestTitl_df[vgBestTitl_cond], 
                        x="Year", 
                        y="Global_Sales", 
                        color = "Publisher",
                        color_discrete_map = colorDict,     
                        labels={"Publisher": "Editeurs",
                        "Global_Sales" : "Ventes total (M$)",
                        "Year": "Année"},
                        title="Meilleur titre de l'année",
                        hover_name="Name")
    
    st.plotly_chart(vgBestTitl)
    
    st.markdown("Ici on peut voir que Nintendo domine avec ses best-sellers. A savoir que l’on à regroupé les même titres sortis sur des consoles différentes. C’est d’ailleurs pour cela qu’un éditeur comme Activision tire son épingle du jeu grâce notamment à sa franchise Call Of Duty sortie sur toutes les consoles respectives selon les années. En comparaison nous avons laissé EA Sports qui restait un gros éditeur des premiers graphiques. Comme on peut le voir, il n’est plus aussi présent.")
    
    vgGenrSals_df = dfVGSales.groupby(['Year','Genre']).agg({"Global_Sales":"sum"}).reset_index(level=['Year','Genre'])

    vgGenrSals = px.bar(vgGenrSals_df, x="Year", y="Global_Sales", color = "Genre", 
                        labels={"Genre": "Genre",
                                "Global_Sales" : "Ventes total (M$)",
                                "Year": "Année"},
                        title="Total des ventes par genres")
    
    st.plotly_chart(vgGenrSals)
    
    st.markdown("La question du genre aurait pu se poser mais aucune vraie tendance ne semble être corrélé au fait de sortir un best sellers. On notera que plus de jeux sport/shooter sont sortis ces dernières années car la technologie fournie par les plateforme le permettait.")
    
    # %%%% Le cas Nintendo  
    
    st.header('Le cas Nintendo')
    st.markdown("Les cas Nintendo est interressant à étudier. Cependant le Dataset de base semble trop pauvre et les données pas forcément pertinente. Notre groupe de travail à donc décider de créer son propre Dataset comme nous le verrons dans la partie méthodologie.")
    
    st.subheader('Notre problèmatique')
    st.markdown("L’impact des réseaux sociaux et des commentaires sur les sites de ventes régissent de plus en plus notre manière de consommer. Mais quand est il pour le marché des jeux vidéos? L’impact est-il si significatif? Peut-on observer des tendances qui font qu’un jeu marche plutôt sur la durée? C’est ce que nous allons vérifier.")
    
    st.subheader('Capture et sélection des données')
    st.markdown("Déroulé du projet :\n - Scrapping des bestsellers de la Nintendo Switch et sélection des jeux à étudier\n - Scrapping des données Twitter \n - Scrapping des commentaires Metacritic et Amazon \n - Text Mining en vue du sentiment Analysis\n - Construction du Dataset final et analyse des données")
    
    st.markdown("<h3 style='text-align: center;'>Peut-on utiliser Twitter comme facteur prédictif des ventes?</h3>", unsafe_allow_html=True)

# %%% Méthodologie

if selectedMenu == "Methodologie":
    
    st.title("Methodologie")
    
    tabn, tabt, tabc, tabm, tabd = st.tabs(["Nintendo", "Twitter", "Commentaires", "Sentiment", "Dataset"])
    
        # %%%% Scrap Switch
        
    with tabn:
        # imageNintendo
        imageNintendo = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Nintendo_red_logo.svg/320px-Nintendo_red_logo.svg.png"
        st.image(imageNintendo,width=250)
        
        st.subheader('Scrapping Nintendo')
        
        st.markdown("Nous avons vu que Nintendo savait vendre des jeux. Nous allons donc scraper leur données et analyser les ventes de ses best sellers. Pour ce faire nous irons directement scrapper les données sur le [site officiel de Nintendo](https://www.nintendo.co.jp/ir/en/finance/software/index.html). Celui-ci liste ses meilleurs jeux par vente totale sur une plateforme pour chaque trimestre. ")
        
        st.markdown("Pour cet exercice, nous nous concentrerons plus tard sur la Switch car ces données d'actualités sont disponibles depuis la création de la console. Mais au départ, nous avons du récupérer les données pour chaque consoles. Aussi pour avoir la dimension temporelle, nous nous aiderons du site [Wayback Machine](http://web.archive.org/). Cet outil permet de retrouver des archives d’autres sites. Ainsi, nous pouvons remonter dans le temps afin de retrouver les meilleures ventes à un moment donné. Petite particularité, la date de l’archive diffère de la date du rapport.")
        
        st.subheader('Sélection des jeux')
        
        st.markdown("Après analyse des bestsellers, nous avons décider de prendre les cinqs meilleurs ventes de la Nintendo Switch. Pour plusieurs raison. \n - **Complétude** : les données sont mieux archivés et sur une plus longue période. Le suivi n'en sera que meilleur. \n -  **Actualité** : les données sont d'actualité et sont des notre problèmatique. \n - **Pertinence** : les données concerne cinq jeu avec des patterns très différents. Cela permettra de comprendre au mieux les facteurs décisifs.")    
        
        # Graphique TOP5
        
        # Création de dfMax
        dfMax = df.groupby("Game").agg({"Sales":"max"}).reset_index().drop([5,6]).sort_values(by="Sales").replace({"POKE":"Pokémon Épée/Bouclier","ACNH":"Animal Crossing : New Horizons","SSBU":"Super Smash Bros. Ultimate","MKD8":"Mario Kart 8 Deluxe","BOTW":"The Legend of Zelda : Breath of the Wild"})
        
        # Création du graphique
        bestFive = go.Figure()
        
        # Images
        imgpokeshield = Image.open("medias/imgpokeshield.png")
        imgbotwlink = Image.open("medias/imgbotwlink.png")
        imgssbumario = Image.open("medias/imgssbumario.png")
        imgacnhnook = Image.open("medias/imgacnhnook.png")
        imgmkd8splt = Image.open("medias/imgmkd8splt.png")
        
        bestFive.add_trace(go.Bar(x = dfMax['Game'], 
                                  y = dfMax['Sales'],
                                  text = dfMax['Sales'],
                                  marker_color = ["crimson","cornflowerblue","lightsteelblue","lightgreen","ivory"],
                                  name = "TOP 5 Nintendo Switch",
                                  hovertemplate = '%{x}'))
        
        # Ajout des images
        bestFive.add_layout_image(dict(source=imgpokeshield,
                                       xref="x",
                                       yref="y",
                                       x=0,
                                       y=1,))

        bestFive.add_layout_image(dict(source=imgbotwlink,
                                       xref="x",
                                       yref="y",
                                       x=1,
                                       y=1,))
        
        bestFive.add_layout_image(dict(source=imgssbumario,
                                       xref="x",
                                       yref="y",
                                       x=2,
                                       y=1,))
        
        bestFive.add_layout_image(dict(source=imgacnhnook,
                                       xref="x",
                                       yref="y",
                                       x=3,
                                       y=1,))
        
        bestFive.add_layout_image(dict(source=imgmkd8splt,
                                       xref="x",
                                       yref="y",
                                       x=4,
                                       y=1,))
        
        bestFive.update_layout_images(dict(sizex=0.9,
                                           sizey=20,
                                           xanchor="center",
                                           yanchor="bottom"))
        
        # Réglages
        bestFive.update_traces(textfont_size=12,
                               textangle=0, 
                               textposition="inside", 
                               cliponaxis=False,
                               showlegend=False,
                               texttemplate = "%{text:.2s}M")
        
        bestFive.update_yaxes(title="Unités vendues (en M)")
        bestFive.update_xaxes(visible=False)
        
        bestFive.update_layout(title="Meilleures ventes de la Nintendo Switch",
                               yaxis=dict(range=[0, 59]))
        
        # Affichage
        st.plotly_chart(bestFive)
        
        
        # %%%% Scrap Twitter
        
    with tabt:
        
        # Image
        st.image("medias/imgtwitter.png",width=250)
        
        st.subheader('Scrap Twitter')
        
        st.markdown(" * insert text here * ")
        
        # %%%% Scrap Comments
        
    with tabc:

        # Scrap Metacritic
        
        # Image
        st.image("medias/imgmetacritic.png",width=250)
        
        st.subheader('Scrap Metacritic')
        st.markdown(" * insert text here * ")        

        # Scrap Amazon
        
        # Image
        st.image("medias/imgamazon.png",width=250)
    
        st.subheader('Scrap Amazon')
        st.markdown(" * insert text here * ")
        
        
        # %%%% Sentiment Analysis
        
    with tabm:
        
        st.subheader('Sentiment Analysis')
        st.markdown(" * insert text here * ")
        
        # %%%% Création du Dataset Final
        
    with tabd:
    
        st.subheader('Dataset Final')
        st.markdown("La particularité de notre dataset final est sa cohérence. En effet les périodes étudiées pour un même jeu n'ont pas la même **périodicité** ni la même **plage** selon leur origine. Nous avons fait le choix de sacrifié un peu de cohérence pour avoir une donnée mensuelle de qualité regroupant le maximum d'information. Ainsi par exemple, nous pourrons voir les effets d'annonces via Twitter avant la commercialisation d'un jeu et les comparer avec le rapport trimestriel officiel de Nintendo.")
        
        # Image
        st.image("medias/imgpipeline.png")
    
# %%% Analyses

if selectedMenu == "Analyses":

    st.title("Analyses")
    
    tabs, tabp, taba, tabm, tabb = st.tabs(["SSBU", "POKE", "ACNH", "MKD8", "BOTW"])
    
    # %%%% SSBU
    with tabs:
        
        # Image
        st.image("medias/bannerssbu.png")
        
        # %%%%% Intro
        
        st.subheader("Un bon exemple ")
        st.markdown("Jeu de combat le plus vendu de l’histoire, Super Smash Bros. Ultimate (SSBU) sera notre porte d’entrée pour notre analyse. En effet, si ses chiffres semblent astronomiques, son pattern représente bien une tendance générales des jeux non présents dans cette étude. Dans le premier graphique, nous pouvons voir les ventes par trimestres du jeu ainsi que son activité Twitter (représenté par la somme des Likes par tweets associés).")
        
        # %%%%% Graph Like/Sales
        
        # Like_SUM et Diff
        ssbuLike = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Like_SUM
        ssbuLike.add_trace(go.Scatter(x = df['Date'][df["Game"]=="SSBU"], 
                                      y = df['Like_SUM'][df["Game"]=="SSBU"],
                                      name = "Likes",
                                      hovertemplate = '%{x|%Y %B}'+
                                                      '<br><b>%{y:.2s}</b> Likes</br>'),
                                     secondary_y=False)
        
        
        # Diff
        ssbuLike.add_trace(go.Scatter(x = df['Date'][df["Game"]=="SSBU"], 
                                      y = df['Diff'][df["Game"]=="SSBU"],
                                      hovertemplate = '%{x|%Y %b}'+
                                                      '<br><b>%{y}M</b> Units</br>',
                                      name = "Ventes",
                                      line_shape='vh',
                                      connectgaps=True),
                                     secondary_y=True)
        
        # Annotation
        
        ssbuLike.add_annotation(x=datetime.date(2018,3,1), 
                                y=100000,
                                text="Annonce de la sortie<br>Nintendo Direct",
                                showarrow=True,
                                arrowhead=1,
                                ax=-30,
                                ay=-10,
                                xanchor="right")
        
        ssbuLike.add_annotation(x=datetime.date(2018,12,1), 
                                y=480000,
                                text="Sortie du jeu",
                                showarrow=True,
                                arrowhead=1,
                                ax=-30,
                                ay=-10,
                                xanchor="right")
        
        ssbuLike.add_annotation(x=datetime.date(2020,1,1), 
                                y=440000,
                                text="DLC Fire Emblem",
                                showarrow=True,
                                arrowhead=1,
                                ax=-30,
                                ay=-30,
                                xanchor="center")
        
        ssbuLike.add_annotation(x=datetime.date(2020,10,1), 
                                y=430000,
                                text="DLC Minecraft",
                                showarrow=True,
                                arrowhead=1,
                                ax=-20,
                                ay=-60,
                                xanchor="center")
        
        ssbuLike.add_annotation(x=datetime.date(2021,10,1), 
                                y=460000,
                                text="DLC Kingdom Hearts",
                                showarrow=True,
                                arrowhead=1,
                                ax=-10,
                                ay=-70,
                                xanchor="center")
        
        # Titre et yRange
        ssbuLike.update_layout(legend=dict(orientation="h"),
                               title_text="Super Smash Bros. Ultimate - Likes et ventes du jeux",
                               yaxis=dict(range=[0, 650000]),
                               yaxis2=dict(tickmode='auto',
                                           range=[0, 13]))
        
        # X-axis Titre
        ssbuLike.update_xaxes(title_text="Date")
        
        
        # Y-axes Titre
        ssbuLike.update_yaxes(title_text="Likes par mois", secondary_y=False)
        ssbuLike.update_yaxes(title_text="Ventes par trimestres (en M)", secondary_y=True)
        
        #Affichage
        st.plotly_chart(ssbuLike)
        
        # ---
        
        # %%%%% Analyse
        
        st.subheader("Un pattern")
        st.markdown("Dans cet exemple, trois choses importantes sont à noter et se confirment pour la plupart des ventes des jeux vidéo : \n - Le premier trimestre est généralement le meilleur, représentant jusqu’à 10 fois les ventes moyennes des trimestres suivants, puis baissant ; \n - Le dernier trimestre de l’année est souvent supérieur aux autres, notamment dû aux fêtes de fin d’année qui représente une bonne opportunité commerciale ; \n - Le confinement lié au COVID19 boostera la ventes des jeux vidéo en général.")
        
        st.subheader("Twitter et les annonces")
        st.markdown("Pour ce qui est de l’activité Twitter, on peu voir la stratégie générale marketing de Nintendo avec ses annonces via les Nintendo Direct. Ces Directs permettent de présenter les nouveautés et les sorties sur leur plateforme. Pour SSBU, on voit son effet d’annonce et ses balbutiements jusqu’à sa sortie. Aussi on pourra noter certains piques d’activité lié aux mis à jour annoncées aux Nintendo Directs. Cependant il ne faut pas confondre activité et sentiment.")
        
        # %%%%% Graph TextBlob
        
        # Sentiment_TEXTBLOB_MEAN
        ssbuBlob = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Like_SUM
        ssbuBlob.add_trace(go.Scatter(x = df['Date'][df["Game"]=="SSBU"], 
                                      y = df['Sentiment_TEXTBLOB_MEAN'][df["Game"]=="SSBU"],
                                      name = "TextBlob",
                                      hovertemplate = '%{x|%Y %B}'+
                                                      '<br><b>%{y}</b></br>'),
                                     secondary_y=False)
        
        # Tendance
        ssbuBlob.add_trace(go.Scatter(x = [datetime.date(2017,1,1),datetime.date(2018,12,1),datetime.date(2021,8,1),datetime.date(2023,1,1)], 
                                      y = [0.9,0.9,0.6,1],
                                      name = "Tendance",
                                      hoverinfo='skip'),
                                     secondary_y=False)
        
        # Annotations
        ssbuBlob.add_annotation(x=datetime.date(2018,12,1), 
                                y=0.9,
                                text="Sortie du jeu",
                                showarrow=True,
                                arrowhead=1,
                                ax=30,
                                ay=-10,
                                xanchor="left")
        
        ssbuBlob.add_annotation(x=datetime.date(2021,8,1), 
                                y=0.6,
                                text="Reprise du<br><b>Smash World Tour</b><br><i>Compétition Esport</i>",
                                showarrow=True,
                                arrowhead=1,
                                ax=30,
                                ay=10,
                                xanchor="left")
        
        # Titre 
        ssbuBlob.update_layout(legend=dict(orientation="h"),
                               title_text="Super Smash Bros. Ultimate - Sentiment Analysis par TextBlob")
        
        # X-axis Titre
        ssbuBlob.update_xaxes(title_text="Date")
        
        # Y-axis Titre
        ssbuBlob.update_yaxes(title_text="Sentiment", secondary_y=False)
        
        st.plotly_chart(ssbuBlob)
        
        # ---
    
        # %%%%% Outro
        
        st.subheader("L’Esport, une renaissance ?")
        st.markdown("Tout d’abord, il faut comprendre que les algorithmes sont mis à mal par les jeux à cause du vocabulaire utilisé par les joueurs. En effet parler d’un jeu de combat, d’action ou d’aventure aura énormément de mots classés normalement comme négatif (par exemple : « death », « punch » ou encore « ennemies »). L’échelle de TextBlob allant de -1 à 1, cela reste un bon score même pour la pointe à 0.4. Ceci étant dit nous pouvons quand même voir des tendances. Sur le graphique si contre par exemple, on peut voir une lassitude s’installant petit à petit jusqu’à la reprise de la scène E-sport de SSBU. Arrêté jusqu’à mi-2021 dû au diverses contraintes liés au COVID19.")
        
        st.subheader("Un pattern symbolique")
        st.markdown("Connaissant ce pattern classique, certains jeux ont décidé une stratégie bien particulière, c’est ce que nous allons voir avec la franchise Pokémon.")
        
        # %%%% POKE
    with tabp:

        # Image
        st.image("medias/bannerpoke.png")
        
        # %%%%% Intro
        
        st.subheader("Une mécanique bien huilée")
        st.markdown("La franchise Pokémon est connue de tous ! Mais peut-on décelée une certaine stratégie derrière cette franchise ? Si Pokémon Épée / Bouclier est le cinquième jeu le plus vendus sur Switch, chaque sortie Pokémon semble battre son record précédent. Regardons les chiffres et tentons de comprendre tout cela. ")
                
        # %%%%% Graph Like/Sales
        
        # Like_SUM / Diff / User Mean
        pokeLike = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Like_SUM
        pokeLike.add_trace(go.Scatter(x = df['Date'][df["Game"]=="POKE"], 
                                      y = df['Like_SUM'][df["Game"]=="POKE"],
                                      name = "Likes",
                                      hovertemplate = '%{x|%Y %B}'+
                                                      '<br><b>%{y:.2s}</b> Likes</br>'),
                                     secondary_y=True)
        
        
        # User Followers count_MEAN
        pokeLike.add_trace(go.Scatter(x = df['Date'][df["Game"]=="POKE"], 
                                      y = df['User Followers count_MEAN'][df["Game"]=="POKE"],
                                      name = "Moyenne des followers",
                                      hovertemplate = '%{x|%Y %B}'+
                                                      '<br><b>%{y:.2s}</b> Follows</br>'),
                                     secondary_y=True)
        
        # Diff
        pokeLike.add_trace(go.Bar(x = df['Date'][df["Game"]=="POKE"], 
                                  y = df['Diff'][df["Game"]=="POKE"],
                                  hovertemplate = '%{x|%Y %b}'+
                                                  '<br><b>%{y}M</b> Units</br>',
                                  name = "Ventes"),
                                 secondary_y=False)
        
        
        # Annotations
        pokeLike.add_annotation(x=datetime.date(2018,11,1), 
                                y=3.6,
                                text="Let's Go, Pikachu / Évoli",
                                showarrow=True,
                                arrowhead=1,
                                ax=-30,
                                ay=-90,
                                xanchor="right")
        
        pokeLike.add_annotation(x=datetime.date(2019,6,1), 
                                y=10,
                                text="Pokémon Direct et E3",
                                showarrow=True,
                                arrowhead=1,
                                ax=-40,
                                ay=-50,
                                xanchor="right")
        
        pokeLike.add_annotation(x=datetime.date(2019,11,1), 
                                y=12.5,
                                text="Épée / Bouclier",
                                showarrow=True,
                                arrowhead=1,
                                ax=-40,
                                ay=-50,
                                xanchor="right")
        
        pokeLike.add_annotation(x=datetime.date(2021,2,1), 
                                y=8.1,
                                text="Annonce de<br>'Legends : Arceus'",
                                showarrow=True,
                                arrowhead=1,
                                ax=-10,
                                ay=-50,
                                xanchor="center")
        
        pokeLike.add_annotation(x=datetime.date(2021,11,1), 
                                y=8,
                                text="Diamant Étincelant / Perle Scintillante<br><i>(remake)</i>",
                                showarrow=True,
                                arrowhead=1,
                                ax=-40,
                                ay=-130,
                                xanchor="right")
        
        pokeLike.add_annotation(x=datetime.date(2022,1,1), 
                                y=14.5,
                                text="Sortie de<br>'Legends : Arceus'",
                                showarrow=True,
                                arrowhead=1,
                                ax=-50,
                                ay=-110,
                                xanchor="right")
        
        pokeLike.add_annotation(x=datetime.date(2022,11,1), 
                                y=29.2,
                                text="Écarlate / Violet",
                                showarrow=True,
                                arrowhead=1,
                                ax=-50,
                                ay=10,
                                xanchor="right")
        
        pokeLike.add_annotation(x=datetime.date(2022,6,1), 
                                y=6,
                                text="<i>estimation</i>",
                                showarrow=True,
                                arrowhead=1,
                                ax=20,
                                ay=-50,
                                xanchor="center")
        
        # Ajout Pokemon Arceus
        pokeLike.add_trace(go.Scatter(x=[datetime.date(2022,3,1),
                                         datetime.date(2022,6,1),
                                         datetime.date(2022,9,1)], 
                                      y=[13.8,1.7,2],
                                      hoverinfo='skip',
                                      mode="lines",
                                      name="Estimation recherche 'Legends : Arceus'"))
        
        # X-axis Titre
        pokeLike.update_xaxes(title_text="Date")
        
        
        # Titre et y Axis Réglages
        pokeLike.update_layout(legend=dict(orientation="h",
                                           yanchor="bottom",
                                           y=-0.3,
                                           xanchor="right",
                                           x=1),
                               title_text="Franchise Pokémon - Ventes et activité Twitter",
                               yaxis=dict(side="right",
                                          range=[0, 30],
                                          title="Ventes totales (en M)"),
                               yaxis2=dict(side="left",
                                          range=[0, 12000000],
                                          title="Like / Followers"),
                               yaxis3=dict(side="left",        
                                           range=[0, 12000000],
                                           overlaying="y",
                                           tickmode="auto"))
        # Affichage          
        st.plotly_chart(pokeLike)
        
        # ---
        
        # %%%%% Analyse
        
        st.subheader("Miser sur la fin d’année")
        st.markdown("On peut voir les ventes totales de la franchise par trimestre mais surtout, on voit que Pokémon ne sort pas n’importe quand. Il profite en effet de l’opportunité des fêtes de fins d’année et de Noël pour sortir pour tous les opus. Un seul déroge à la règle, c’est Pokémon Legends : Arceus qui sortira le 28 janvier 2022. D’ailleurs, lors du scrapping, il ne sera pas présent n’étant pas dans les top ventes pour Nintendo (même si il bat certains record de ventes lors de sa première semaine). Ainsi on peut voir l’importance pour Pokémon de sortir à la bonne période pour maximiser ses ventes !")
        
        st.subheader("Une grande communauté")
        st.markdown("La communauté Pokémon est tout simplement énorme, bien que le scrapping récupère la communauté pokémon général, on voit des tendances fortes. Le nombre de likes est astronomique ! Notons le fait que chaque opus sortis ramène toujours plus de Likes. Mais si on regarde le nombre de follower moyen, on peut distinguer une certaine lassitude au fil du temps. Lassitude qui se remarquera d’autant plus sur le sentiment analysis.")
        
        # %%%%% Graph Vader/TextBlob
        
        # Sentiment analysis
        pokeSent = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Sentiment_VADER_MEAN
        pokeSent.add_trace(go.Scatter(x = df['Date'][df["Game"]=="POKE"], 
                                      y = df['Sentiment_VADER_MEAN'][df["Game"]=="POKE"],
                                      hovertemplate = '%{x|%Y %b}'+
                                                      '<br><b>%{y:.3f}</b></br>',
                                      name = "Vader"),
                                     secondary_y=False)
        
        # Sentiment_TEXTBLOB_MEAN
        pokeSent.add_trace(go.Scatter(x = df['Date'][df["Game"]=="POKE"], 
                                      y = df['Sentiment_TEXTBLOB_MEAN'][df["Game"]=="POKE"],
                                      name = "Textblob",
                                      hovertemplate = '%{x|%Y %B}'+
                                                      '<br><b>%{y:.3f}</b></br>'),
                                     secondary_y=True)
        
        # Sentiment Tendance
        pokeSent.add_trace(go.Scatter(x = [datetime.date(2018,11,1),
                                           datetime.date(2019,11,1),
                                           datetime.date(2020,11,1),
                                           datetime.date(2021,11,1),
                                           datetime.date(2022,1,1),
                                           datetime.date(2023,1,1)], 
                                      y = [0.3,0.26,0.23,0.27,0.21,0.21],
                                      hoverinfo='skip',
                                      name = "Tendance",
                                      mode="lines"),
                                     secondary_y=False)
        
        # Highlight Pokemon "Let's Go, Pikachu / Évoli"
        pokeSent.add_vrect(x0=datetime.date(2018,11,1), x1=datetime.date(2019,11,1), 
                           annotation_text="Let's Go<br>Pikachu / Évoli", 
                           annotation_position="top right",  
                           annotation_font_size=11,
                           annotation_font_color="Black",
                           fillcolor="yellow", opacity=0.1, line_width=0)
        
        # Highlight Pokemon "remake"
        pokeSent.add_vrect(x0=datetime.date(2019,11,1), x1=datetime.date(2021,11,1), 
                           annotation_text="Épée / Bouclier", 
                           annotation_position="top right",  
                           annotation_font_size=11,
                           annotation_font_color="Black",
                           fillcolor="green", opacity=0.1, line_width=0)
        
        # Highlight Pokemon "Arceus"
        pokeSent.add_vrect(x0=datetime.date(2022,1,1), x1=datetime.date(2023,1,1), 
                           annotation_text="Legends : Arceus", 
                           annotation_position="top right",  
                           annotation_font_size=11,
                           annotation_font_color="Black",
                           fillcolor="blue", opacity=0.1, line_width=0)
        
        # X-axis Titre
        pokeSent.update_xaxes(title_text="Date")
        
        # Titre et y Axis Réglages
        pokeSent.update_layout(legend=dict(orientation="h"),
                               title_text="Franchise Pokémon - Sentiment Analysis",
                               yaxis=dict(side="right",
                                          range=[0.1, 0.4],
                                          title="Vader"),
                               yaxis2=dict(side="left",
                                          range=[0, 0.6],
                                          title="TextBlob"))
        # Affichage          
        st.plotly_chart(pokeSent)
        
        # ---
            
        # %%%%% Outro
        
        st.subheader("Un nouveau jeu à l’ancienne")
        st.markdown("Sur ce graph nous voyons encore une fois la lassitude qui s’installe au fil du temps. Vader et TextBlob sont deux modèles différents qui offriront à peu prêt les même tendance au fil du temps selon leur échelle respective. Il faut noter que Legends : Arceus est un pokémon bien particulier qui aura tenté des choses nouvelles sur son gameplay. Malheureusement « nouveautés » n’est pas forcément gage de « qualité ».")
        
        st.subheader("Les vieux pots")
        st.markdown("Même si on dénote une lassitude, les ventes Pokémon sont toujours au beau fixe. Jusqu’à 20.6M pour le premier trimestre de Pokémon Ecarlate / Violet qui reprend les mécaniques de bases de la franchise (qu’elles soient marketing ou sur le gameplay). Les jeux Pokémon ne doivent pas sortir de leur axe pour marcher efficacement et toujours agrandir leur communauté.  Mais est-ce qu’une grande communauté est toujours une bonne pub ? C’est ce que nous allons voir avec Animal Crossing.")
        
    # %%%% ACNH
    with taba:

        # Image
        st.image("medias/banneracnh.png")
        
        # %%%%% Intro
        
        st.subheader("Le feu des projecteurs")
        st.markdown("Animal Crossing : New Horizons (ACNH) est un jeu « niche » dans le monde du jeu vidéo. Deux facteurs principaux ont catapulté sa vente : sa sortie en plein confinement et sa mise en lumière par la presse spécialisée. Mais si les joueurs niches ont adorés, qu’en est-il des joueurs en général ? ")
        
        # %%%%% Graph Like/Sales

        # Like_SUM et Diff
        acnhLike = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Like_SUM
        acnhLike.add_trace(go.Scatter(x = df['Date'][df["Game"]=="ACNH"], 
                                      y = df['Like_SUM'][df["Game"]=="ACNH"],
                                      name = "Likes",
                                      hovertemplate = '%{x|%Y %B}'+
                                                      '<br><b>%{y:.2s}</b> Likes</br>'),
                                     secondary_y=False)
        
        acnhLike.add_annotation(x=datetime.date(2019,6,1), 
                                y=190000,
                                text="Nintendo Direct<br>Annonce sortie",
                                showarrow=True,
                                arrowhead=1,
                                ax=20,
                                ay=-80,
                                xanchor="left")
        
        acnhLike.add_annotation(x=datetime.date(2020,3,1), 
                                y=1500000,
                                text="Sortie du jeu",
                                showarrow=True,
                                arrowhead=1,
                                ax=30,
                                ay=10,
                                xanchor="left")
        
        acnhLike.add_annotation(x=datetime.date(2021,3,1), 
                                y=383500,
                                text="Update 1.8<br>'Super Mario 35 ans'",
                                showarrow=True,
                                arrowhead=1,
                                ax=30,
                                ay=-100,)
        
        acnhLike.add_annotation(x=datetime.date(2021,10,1), 
                                y=287100,
                                text="Annonce du DLC<br>'Happy Home Paradise'",
                                showarrow=True,
                                arrowhead=1,
                                ax=30,
                                ay=-60,)
        
        # Diff
        acnhLike.add_trace(go.Scatter(x = df['Date'][df["Game"]=="ACNH"], 
                                      y = df['Diff'][df["Game"]=="ACNH"],
                                      hovertemplate = '%{x|%Y %b}'+
                                                      '<br><b>%{y}M</b> Units</br>',
                                      name = "Ventes",
                                      line_shape='vh',
                                      connectgaps=True),
                                     secondary_y=True)
        
        # Titre et yRange
        acnhLike.update_layout(legend=dict(orientation="h"),
                               title_text="Animal Crossing: New Horizons - Likes et ventes du jeux",
                               yaxis=dict(range=[0, 1600000]),
                               yaxis2=dict(tickmode='auto',
                                           range=[0, 16]))
        
        # X-axis Titre
        acnhLike.update_xaxes(title_text="Date")
        
        # Y-axes Titre
        acnhLike.update_yaxes(title_text="Likes par mois", secondary_y=False)
        acnhLike.update_yaxes(title_text="Ventes par trimestres (en M)", secondary_y=True)
        
        #Affichage
        st.plotly_chart(acnhLike)
        
        # ----
        
        # %%%%% Analyse
        
        st.subheader("Un bon départ")
        st.markdown("Ici on peut voir l’énorme activité d’ACNH avant et pendant sa sortie. Après la franchise Pokémon (qui ne comprends pas que les jeux vidéo) ACNH atteint un maximum de 1.5M de likes devant tous les autres jeux étudiés.")
        
        st.subheader("Un ralentissement visible")
        st.markdown("ACNH restera premier des ventes par trimestres pendant un an puis va décéléré de plus en plus. On peut voir que la sortie du DLC payant « Happy Home Paradise » en Novembre 2021, en plus de sortir en fin d’année, boostera un peu les ventes. Cependant on vient bien qu’il y a une grosse baisse d’activité. Essayons de comprendre pourquoi.")
        
        # %%%%% Graph MTC
        
        # Metacritic Count and Mean
        acnhMtc = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Mean
        acnhMtc.add_trace(go.Scatter(x = df['Date'][df["Game"]=="ACNH"], 
                                      y = df['meanMTC'][df["Game"]=="ACNH"],
                                      name = "Moyenne",
                                      hovertemplate = '%{x|%Y %B}'+
                                                      '<br><b>%{y}</b> /10</br>'),
                                     secondary_y=True)
        
        # Count
        acnhMtc.add_trace(go.Bar(x = df['Date'][df["Game"]=="ACNH"], 
                                      y = df['countMTC'][df["Game"]=="ACNH"],
                                      hovertemplate = '%{x|%Y %b}'+
                                                      '<br><b>%{y}</b> comments</br>',
                                      name = "Quantité",
                                      yaxis='y2'),
                                     secondary_y=False)
        
        
        
        # Annotation
        
        acnhMtc.add_annotation(x=datetime.date(2020,5,1), 
                                y=500,
                                text="<b>2026</b> : 2020 Mars <br><b>552</b> : 2020 Avril</br>",
                                showarrow=True,
                                arrowhead=1,
                                ax=20,
                                ay=50,
                                xanchor="left")
        
        # Titre et yRange
        acnhMtc.update_layout(legend=dict(orientation="h"),
                              title_text="Animal Crossing: New Horizons - Evolution des commentaires Metacritic",
                              hovermode="x unified",
                              yaxis=dict(range=[0, 500]),
                              yaxis2=dict(tickmode='auto',
                                           range=[0, 10],
                                          overlaying='y'))
        # Affichage
        st.plotly_chart(acnhMtc)
        
        # ----
        
        # %%%%% Outro
        
        st.subheader("Un jeu prisé mais mal aimé")
        st.markdown("Si vous n’êtes pas habitué aux notes dans les jeux vidéo, sachez que 6 n’est pas très bon. En regardant ce graphique vous comprendrez alors qu’ACNH n’a pas été bien accueilli par les joueurs. Et c’est grâce à ça que l’on comprend que le confinement et l’effet de mode a joué en faveur des ventes d’ACNH. Cependant une fois acheté et testé, énormément de joueurs n’ont pas compris le but du jeu et l’ont bien fait comprendre sur différents réseaux. Il faudra attendre presque un an pour atteindre enfin 6/10 de moyenne (devenir un jeu correct).")
        
        st.subheader("Peut-on prévoir ?")
        st.markdown("Enfaite, ACNH a été victime de son succès. Cela se voit aussi par l’augmentation de la note moyenne au fil du temps. Après l’effet de mode, les joueurs savaient dans quoi ils « s’embarquaient ». La tendance s’inverse alors petit à petit. Mais alors peut-on prévoir les ventes et/ou les notes de jeu grâce au réseau sociaux ? Peut-on émettre une « metric », un « facteur » ou un algorithme qui pourrait nous aider à prévoir. Mario Kart Deluxe 8 a peut-être la réponse à cette question.")
        
    # %%%% MKD8
    with tabm:

        # Image
        st.image("medias/bannermkd8.png")
        
        # %%%%% Intro
        
        st.subheader("Un classique")
        st.markdown("La franchise Mario Kart est un classique. Chaque console Nintendo depuis la super NES à eu le droit à son opus. Attendu au tournant, les développeurs ont pris le parti cette fois de sortir un bon jeu et de continuer à le développer dans une politique de Game as Service avec de nombreux contenus additionnels. Il faut rappeler que Mario Kart 8 Deluxe (MKD8) est un remake de Mario Kart 8 sorti sur WiiU.")
        
        # %%%%% Graph Like/Sales
        
        # Like_SUM et Diff
        mkd8Like = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Like_SUM
        mkd8Like.add_trace(go.Scatter(x = df['Date'][df["Game"]=="MKD8"], 
                                      y = df['Like_SUM'][df["Game"]=="MKD8"],
                                      name = "Likes",
                                      hovertemplate = '%{x|%Y %B}'+
                                                      '<br><b>%{y:.2s}</b> Likes</br>'),
                                     secondary_y=False)
        
        # Annotations
        mkd8Like.add_annotation(x=datetime.date(2017,4,1), 
                                y=33000,
                                text="Sortie du jeu",
                                showarrow=True,
                                arrowhead=1,
                                ax=40,
                                ay=-90,
                                xanchor="left")
        
        mkd8Like.add_annotation(x=datetime.date(2022,3,1), 
                                y=165000,
                                text="V2.0<br><i>Mise à jour</i>",
                                showarrow=True,
                                arrowhead=1,
                                ax=-30,
                                ay=10,
                                xanchor="right")
        
        # Highlight augmentation likes 
        mkd8Like.add_vrect(x0=datetime.date(2021,4,1), x1=datetime.date(2022,12,1), 
                           annotation_text="Augmentation de l'activité Twitter", 
                           annotation_position="top right",  
                           annotation_font_size=11,
                           annotation_font_color="Black",
                           fillcolor="green", opacity=0.1, line_width=0)
        
        
        # Diff
        mkd8Like.add_trace(go.Scatter(x = df['Date'][df["Game"]=="MKD8"], 
                                      y = df['Diff'][df["Game"]=="MKD8"],
                                      hovertemplate = '%{x|%Y %b}'+
                                                      '<br><b>%{y}M</b> Units</br>',
                                      name = "Ventes",
                                      line_shape='vh',
                                      connectgaps=True),
                                     secondary_y=True)
        
        # Titre et yRange
        mkd8Like.update_layout(legend=dict(orientation="h"),
                               title_text="Mario Kart 8 Deluxe - Likes et ventes du jeux",
                               yaxis=dict(range=[0, 180000]),
                               yaxis2=dict(tickmode='auto',
                                           range=[0,9]))
        
        # X-axis Titre
        mkd8Like.update_xaxes(title_text="Date")
        
        
        # Y-axes Titre
        mkd8Like.update_yaxes(title_text="Likes par mois", secondary_y=False)
        mkd8Like.update_yaxes(title_text="Ventes par trimestres (en M)", secondary_y=True)
        
        #Affichage
        st.plotly_chart(mkd8Like)
        
        # ---
        
        # %%%%% Analyse
        
        st.subheader("Une progression positive")
        st.markdown("Comment savoir que c’est un bon jeu ? Les ventes augmentent au fur et à mesure du temps (hors sortie et pour chaque trimestre). Depuis notre étude, c’est la première fois que cela se produit. Mais qu’en est-il de Twitter ?")
        
        st.subheader("Twitter hors cible")
        st.markdown("Comme vous pouvez le voir, l’activité Twitter est au plus bas ! Ce « partygame » familial a surement dû préférer orienter son marketing vers des plateformes plus familial (spot TV par exemple). Pour notre étude, on est presque aveugle. Mais cela veut dire que les joueurs en cible ne sont pas sur Twitter. Et ça MKD8 l’avait compris dès le départ. Cependant, plus de gens achetaient MKD8, plus de potentiel Twitter existait. C’est comme cela que l’on peut remarquer une hausse au milieu de 2021. Le maximum aura fait parler de lui car les nombreux joueurs ont partager les informations autour de la mise-à-jour V.2.0 tant attendue.")
        
        # %%%%% Graph TextBlob/Sales
        
        # La force tranquille
        
        # Création de dfcomp
        dfcomp = df.groupby("Game").agg({"Like_SUM":"sum","Sales":"max","Diff":"mean",'Sentiment_TEXTBLOB_MEAN':"mean"}).sort_values(by="Sales",ascending=False).drop(['SWCH','TOTL']).reset_index()
        dfcomp = dfcomp.rename(columns={"Sentiment_TEXTBLOB_MEAN": "TextBlob Note"})
        
        # Marker avec couleur selon la note
        mkd8Sent = px.scatter(dfcomp, x="Like_SUM", y="Sales", hover_name="Game",
                              log_x=True,
                              color="TextBlob Note",
                              color_continuous_scale="Rdylgn",
                              hover_data={'Game':False,
                                          'TextBlob Note':':.3',
                                          'Like_SUM':':.2s',
                                          'Sales':':.2f'})
        
        mkd8Sent.update_traces(marker=dict(size=16, symbol="diamond"),
                               selector=dict(mode="markers"))
        
        # Text au niveau des markers
        mkd8Sent.add_trace(go.Scatter(x=dfcomp["Like_SUM"],
                                      y=dfcomp["Sales"],
                                      text=dfcomp["Game"],
                                      mode="text",
                                      name="Lines and Text",
                                      texttemplate="<br><b>%{text}</b><br>%{y:.2s}M units<br>%{x:.2s} Likes<br>",
                                      textposition=["bottom right",
                                                    "top right",
                                                    "top left",
                                                    "bottom right",
                                                    "top left"]))
        
        # Titre et yRange
        mkd8Sent.update_layout(legend=dict(orientation="h"),
                               title_text="Mario Kart 8 Deluxe - La force tranquille")
        
        # X-axis Titre
        mkd8Sent.update_xaxes(title_text="Likes sur toute la période")
        
        # Y-axes Titre
        mkd8Sent.update_yaxes(title_text="Vente totale (en M)")
        
        # Masquage de la légende
        mkd8Sent.update_traces(showlegend=False)
        
        # Affichage
        st.plotly_chart(mkd8Sent)
        
        # ---
        
        # %%%%% Outro
        
        st.subheader("Une communauté uniquement de fan")
        st.markdown("Au final, ceux qui communiquent sur Twitter sont très peu mais son des fans du jeu. Sur ce graphique, on peut voir le sentiment analysis selon l’API TextBlob. Alors, comme dit auparavant pour Super Smash Bros. Ultimate (SSBU), il faut le prendre avec des pincettes. Mais on voit clairement la tendance au vert pour MK8D alors que la communauté n’a que très peu d’activités.")
        
        st.subheader("Les réseaux sociaux, un outil")
        st.markdown("On a pu voir que chacun des jeux présentés ont eu des patterns différents. Au final, on commence à comprendre que le réseaux social Twitter ne doit pas être vu comme un facteur mais comme un plus comme un outil qui servirait à comprendre et à vendre son jeu. Et si un bon élève utiliserait cet outil, que se passerait-il ?")
        
    # %%%% BOTW
    with tabb:

        # Image
        st.image("medias/bannerbotw.png")
        
        # %%%%% Outro
        
        st.subheader("Chef d’œuvre")
        st.markdown("The Legend of Zelda : Breath Of The Wild (BOTW) est un jeu très populaire qui a su durer dans le temps. Marathonien des ventes, il n’atteint aucun chiffre astronomique mais il sera en cible sur tout son parcours. C’est ainsi qu’il reste toujours en quatrième position alors que son premier trimestre n’atteignait que faiblement 2.76M (jeux au plus faible lancement parmi tout ceux étudié).")
            
        # %%%%% Graph Camembert

        # Sortie du jeu attendu 
        labels = ['Nintendo Switch','Others Software','Breath Of The Wild']
        values = [2.74,2.7,2.76]
        
        # Camembert
        botwPreS = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0, 0, 0.2])])
        
        # Personnalisation
        botwPreS.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=16,
                               showlegend=False)
        
        # Titre
        botwPreS.update_layout(title_text="The Legend of Zelda: Breath of the Wild - Ventes selon Nintendo au 30 Mars 2017")
        
        #Affichage
        st.plotly_chart(botwPreS)
        
        # ---
        
        # %%%%% Commentaire
        
        st.subheader("Un jeu attendu")
        st.markdown("Pour comprendre à quel point BOTW a été attendu, il faut regarder du point de vue des ventes lors du premier mois. Les chiffres sont aux bons endroits, il y a eu plus de jeu BOTW vendus que de Switch pour le faire fonctionner. Fait très rare, on peut lier à la manie de certains d’acheter une version normale et une version collector lorsque l’on sait qu’il sera bon. Et de se point de vue, BOTW ne laisse personne indifférent.")
        
        # %%%%% Graph Notes

        # Notation MTC et AMAZON
        botwNote = make_subplots(rows=1, cols=2,
                                 subplot_titles=("Metacritic", "Amazon"))
        
        botwNote.add_trace(go.Bar(x=dfmean["Game"], y=dfmean["countMTC"],
                                  marker=dict(color=dfmean["meanMTC"], 
                                              coloraxis="coloraxis"),
                                  name="Metacritic",
                                  hovertemplate = '%{x}'+
                                                  '<br>%{text:.1f}/10</br>'+
                                                  "%{y:.2s} comments",
                                  text=dfmean["meanMTC"],
                                  texttemplate = "%{text:.2f}"),
                           row=1, col=1)
        
        botwNote.add_trace(go.Bar(x=dfmean["Game"], y=dfmean["countAMZ"],
                                  marker=dict(color=dfmean["meanAMZ"], 
                                              coloraxis="coloraxis"),
                                  name="Amazon",
                                  hovertemplate = '%{x}'+
                                                  '<br>%{text:.1f}/10</br>'+
                                                  "%{y:.2s} comments",
                                  text=dfmean["meanAMZ"],
                                  texttemplate = "%{text:.2f}"),
                           row=1, col=2)
        
        # Y-axes
        botwNote.update_yaxes(title_text="Quantité",range=[0, 6000], row=1, col=1)
        botwNote.update_yaxes(title_text="Quantité",range=[0, 9000], row=1, col=2)
        
        # Legend
        botwNote.update_layout(legend=dict(orientation="h",
                                           yanchor="bottom",
                                           y=1.1,
                                           xanchor="right",
                                           x=1))
        botwNote.update_traces(textfont_size=12,
                               textangle=0, 
                               textposition="outside", 
                               cliponaxis=False,
                               showlegend=False)
        
        # Titre
        botwNote.update_layout(legend=dict(orientation="h"),
                               title_text="The Legend of Zelda: Breath of the Wild - Notes émises par le publique (/10)",
                               coloraxis=dict(colorscale='Rdylgn'))
        
        st.plotly_chart(botwNote)
        
        # ---
        
        # %%%%% Analyse
        
        st.subheader("Ovation du public")
        st.markdown("Au-delà de la quantité astronomique des notes déposées sur Metacritic ou Amazon, le fait remarquable est que la moyenne reste la plus haute malgré cela ! Qui plus est, internet a cet effet de ne voir apparaitre que l’avis des joueurs mécontents. Ce qui se vérifie bien sur le site Metacritic avec Animal Crossing : New Horizons qui se fait descendre par la critique ou encore Pokémon Épée / Bouclier qui peine avec ses 6.38 de moyennes. Ici, BOTW trône fièrement avec plus de 5 000 commentaires avec 9 de moyenne ! Notons que l’avis Amazon est quelque peu biaisé, en effet beaucoup de commentaire et notes associés concerne les livraisons. Mais même avec ça, BOTW reste bien au-dessus. Observons maintenant les ventes et l’activité Twitter.")
        
        # %%%%% Graph Like/Sales

        # Like_SUM et Diff
        botwLike = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Like_SUM
        botwLike.add_trace(go.Scatter(x = df['Date'][df["Game"]=="BOTW"], 
                                      y = df['Like_SUM'][df["Game"]=="BOTW"],
                                      name = "Likes",
                                      hovertemplate = '%{x|%Y %B}'+
                                                      '<br><b>%{y:.2s}</b> Likes</br>'),
                                     secondary_y=False)
        
        # Regression Polynomiale
        x = df['Date'][df['Game'] == 'BOTW'].apply(lambda date: date.toordinal())
        y = df['Like_SUM'][df["Game"]=="BOTW"]
        # Polynomiale de degré 3
        coeffs = np.polyfit(x, y, 3)
        trendline = coeffs[0] * x**3 + coeffs[1] * x**2 + coeffs[2] * x + coeffs[3]
        
        botwLike.add_trace(go.Scatter(x=df['Date'][df["Game"]=="BOTW"], 
                                      y=trendline,
                                      name="Tendance des likes",
                                      hoverinfo='skip'))
        
        
        # Diff
        botwLike.add_trace(go.Scatter(x = df['Date'][df["Game"]=="BOTW"], 
                                      y = df['Diff'][df["Game"]=="BOTW"],
                                      hovertemplate = '%{x|%Y %b}'+
                                                      '<br><b>%{y}M</b> Units</br>',
                                      name = "Ventes",
                                      line_shape='vh',
                                      connectgaps=True),
                                     secondary_y=True)
        
        # Annotation
        botwLike.add_annotation(x=datetime.date(2019,6,1), 
                                y=490000,
                                text="Annonce de <br>'Tears Of The Kingdom'",
                                showarrow=True,
                                arrowhead=1,
                                ax=-30,
                                ay=10,
                                xanchor="right")
        
        botwLike.add_annotation(x=datetime.date(2016,6,1), 
                                y=62000,
                                text="Annonce<br>lors de l'E3",
                                showarrow=True,
                                arrowhead=1,
                                ax=30,
                                ay=-90,
                                xanchor="center")
        
        botwLike.add_annotation(x=datetime.date(2017,3,1), 
                                y=310000,
                                text="Sortie du jeu",
                                showarrow=True,
                                arrowhead=1,
                                ax=30,
                                ay=-10,
                                xanchor="left")
        
        botwLike.add_annotation(x=datetime.date(2021,3,1), 
                                y=470000,
                                text="Annonce de <br>'Skyward Sword HD'",
                                showarrow=True,
                                arrowhead=1,
                                ax=-20,
                                ay=30,
                                xanchor="right")
        
        botwLike.add_annotation(x=datetime.date(2021,6,1), 
                                y=370000,
                                text="Informations sur<br>'Tears Of The Kingdom'",
                                showarrow=True,
                                arrowhead=1,
                                ax=40,
                                ay=-30,
                                xanchor="left")
        
        botwLike.add_annotation(x=datetime.date(2022,1,1), 
                                y=340000,
                                text=" ",
                                showarrow=True,
                                arrowhead=1,
                                ax=20,
                                ay=-30,
                                xanchor="left")
        
        
        # Titre et yRange
        botwLike.update_layout(legend=dict(orientation="h",
                                           yanchor="bottom",
                                           y=-0.3,
                                           xanchor="right",
                                           x=1),
                               title_text="The Legend of Zelda: Breath of the Wild - Likes et ventes du jeux",
                               yaxis=dict(range=[0, 500000]),
                               yaxis2=dict(tickmode='auto',
                                           range=[0, 5]))
        
        # X-axis Titre
        botwLike.update_xaxes(title_text="Date")
        
        # Y-axes Titre
        botwLike.update_yaxes(title_text="Likes par mois", secondary_y=False)
        botwLike.update_yaxes(title_text="Ventes par trimestres (en M)", secondary_y=True)
        
        #Affichage
        st.plotly_chart(botwLike)
        
        # ----
        
        # %%%%% Outro
        
        st.subheader("Une petite communauté active")
        st.markdown("Si les ventes stagnent au fil du temps, on remarque une vraie tendance au niveau de l’activité Twitter. Attisant la curiosité des nouveaux joueurs ayant entendu parler de se jeu si bien noté, on peut comprendre que BOTW a su gagner de plus en plus de publique. Un moyen de bien le voir est par la différence entre l’annonce du premier BOTW (62K Likes) et l’annonce de sa suite The Legend of Zelda : Tears Of The Kingdom (TOTK) qui culmine à 490k Likes ! Et chaque nouvelle information fuitant créera un nouveau pique d’activité pour ce deuxième opus.")
        
        # Données
        botw_z01 = ["Ocarina of Time (1998)","Majora's Mask (2000)"]
        botw_z02 = ["Breath of the Wild (2017)","Tears of the Kingdom (2023)"]
        botw_s01 = [7.6,3.36]
        botw_s02 = [29,0]
        
        # Images
        imgocarina = Image.open("medias/imgocarina.png")
        imgskullkid = Image.open("medias/imgskullkid.png")
        imgbotwlink = Image.open("medias/imgbotwlink.png")
        imgtotkmark = Image.open("medias/imgtotkmark.png")
        
        botwprev = make_subplots(rows=1, cols=2,
                                 subplot_titles=("Nintendo 64","Nintendo Switch"))
        
        botwprev.add_trace(go.Bar(x = botw_z01, 
                                  y = botw_s01,
                                  marker_color = ["#2ecc71","#af7ac5"]),
                                  row=1, col=1)
        
        botwprev.add_trace(go.Bar(x = botw_z02, 
                                  y = botw_s02,
                                  marker_color = ["cornflowerblue","grey"]),
                                  row=1, col=2)
        
        botwprev.update_traces(textfont_size=18,
                               textangle=0, 
                               textposition="inside", 
                               cliponaxis=False,
                               showlegend=False,
                               texttemplate = "               %{y:.2s}M")
        
        botwprev.add_layout_image(dict(source=imgocarina,
                                       xref="x",
                                       x=-0.1,
                                       y=0.02,))
        
        botwprev.add_layout_image(dict(source=imgskullkid,
                                       xref="x",
                                       x=0.8,
                                       y=0.02,))
        
        botwprev.add_layout_image(dict(source=imgbotwlink,
                                       xref="x2",
                                       x=-0.1,
                                       y=0.02,))
        
        botwprev.add_layout_image(dict(source=imgtotkmark,
                                       xref="x2",
                                       x=1,
                                       y=0.02,))
        
        botwprev.update_layout_images(dict(sizex=0.9,
                                           sizey=0.5,
                                           xanchor="center",
                                           yanchor="bottom"))
        
        
        botwprev.update_layout(title="The Legend of Zelda, seconds opus et prévisions",
                               yaxis=dict(range=[0, 9],
                                          title="Ventes en M$"),
                               yaxis2=dict(range=[0, 35],
                                           title="Ventes en M Units"))

        st.plotly_chart(botwprev)
        
        st.subheader("Un nouveau cycle")
        st.markdown("Si BOTW fut un franc succès tant par la critique que par ses notes, on voit bien que le publique intègre de plus en plus le nouveau titre (TOTK) en délaissant l’ancien sur l’activité Twitter. Si on ne peut pas prévoir exactement les ventes de celui-ci sur la durée. On peut tout de même deviner que sa sortie le 12 mai 2023 sera un énorme succès et qu’il va exploser les ventes de son prédécesseur.")
        st.markdown("Cependant ses ventes totales ne seront pas forcément meilleures que le premier opus. Effectivement, la série Zelda a déjà connu un cas similaire avec The Legend of Zelda: Ocarina of Time. Là encore succès incontestable dans le monde du jeu vidéo, sa suite The Legend of Zelda: Majora's Mask aura explosé les ventes lors de sa sortie mais aura été vendu presque deux fois moins que son prédécesseur (chiffres du premier dataset). Être une suite direct n’est pas forcément une bonne stratégie et sortir de sa timeline pour le prochain opus est des fois une meilleure stratégie.")
        
# %%% Conclusion

if selectedMenu == "Conclusion":
    st.title("Twitter ?")
    
    st.subheader("Un outil mais pas une métric fiable")
    st.markdown("On ne peut émettre de prévision des ventes directement grâce à Twitter. Cependant, on peut y déceler des tendances. Twitter reste un très bon moyen de « prendre la température » lors d’annonces et d’évènement pour voir si le publique répond positivement ou négativement à celles-ci.")
    
    st.subheader("Marketing et Développement")
    st.markdown("Les réseaux sociaux sont un outil incontournable pour toucher le maximum de personne ! C’est indéniable mais pour durer dans le temps, les éditeurs doivent penser à cibler leur publique tant par le gameplay que par les outils utilisés. Il faudra donc mettre les équipes marketing en phase avec les développeurs pour une bonne efficacité. C’est comme cela qu’un jeu, connaitra un succès.")

# %%% Scrapp-App

if selectedMenu == "Scrap-App":
    st.title("Incomming !")
    st.subheader('voilà voilà')
