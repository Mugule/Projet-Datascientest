
# %% (_.~" IMPORT "~._) 

import datetime
import numpy as np
import pandas as pd
import matplotlib.dates as mdates

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


# %%% Import de df
df = pd.read_csv("finalDataset.csv")
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


# %% (_.~" STREAMLIT "~._) 

with st.sidebar:
    selectedMenu = option_menu(
        menu_title = "Switch bestsellers",
        menu_icon= "nintendo-switch",
        options = ["Contexte",
                   "Methodologie",
                   "Analyses",
                   "Conclusion",
                   "Scrap-App"],
        icons = ["info",
                 "cloud-download",
                 "graph-up",
                 "controller",
                 "twitter"])


# %%% Contexte

if selectedMenu == "Contexte":
    
    st.title("Contexte")
    
    st.caption('_ - Promotion JAN 2023 Datascientest - _') 


# %%% Méthodologie

if selectedMenu == "Methodologie":
    
    st.title("Comment qu'on a fait")
    
    
    
# %%% Analyses

if selectedMenu == "Analyses":

    st.title("Let's see what we got here")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["SSBU", "POKE", "ACNH", "MKD8", "BOTW"])
    
    # %%%% SSBU
    with tab1:
        st.header("Super Smash Bros. Ultimate")
        st.caption("2018 Dec 7 – 30 M Units (#3)")
        
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
    with tab2:
        st.header("Franchise Pokémon")
        st.caption("2020 Dec 20 – 36 M Units (#5) \n Chiffres pour Épée / Bouclier ")
        
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
                                ax=-40,
                                ay=-130,
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
        pokeLike.update_layout(legend=dict(orientation="h"),
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
    with tab3:
        st.header("Animal Crossing : New Horizons")
        st.caption("2020 Mar 20 – 42 M Units (#2)")
        
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
    with tab4:
        st.header("Mario Kart 8 Deluxe")
        st.caption("2020 Avr 27 – 52 M Units (#1)")
        
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
    with tab5:
        st.header("The Legend of Zelda : Breath of the Wild")
        st.caption("2017 Mar 3 – 29 M Units (#4)")
        
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
        x = mdates.date2num(df['Date'][df["Game"]=="BOTW"])
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
        botwLike.update_layout(legend=dict(orientation="h"),
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
        
        st.subheader("Un nouveau cycle")
        st.markdown("Si BOTW fut un franc succès tant par la critique que par ses notes, on voit bien que le publique intègre de plus en plus le nouveau titre (TOTK) en délaissant l’ancien sur l’activité Twitter. Si on ne peut pas prévoir exactement les ventes de celui-ci sur la durée. On peut tout de même deviner que sa sortie le 12 mai 2023 sera un énorme succès et qu’il va exploser les ventes de son prédécesseur.\nCependant ses ventes totales ne seront pas forcément meilleures que le premier opus. Effectivement, la série Zelda a déjà connu un cas similaire avec The Legend of Zelda: Ocarina of Time. Là encore succès incontestable dans le monde du jeu vidéo, sa suite The Legend of Zelda: Majora's Mask aura explosé les ventes lors de sa sortie mais aura été vendu presque deux fois moins que son prédécesseur (chiffres du premier dataset). Être une suite direct n’est pas forcément une bonne stratégie et sortir de sa timeline pour le prochain opus est des fois une meilleure stratégie.")
        
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


