import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
import time
import plotly.graph_objects as go
from plotly.graph_objs import *


#%% Fond d'écran

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url("https://cdn.pixabay.com/photo/2020/06/19/22/33/wormhole-5319067_960_720.jpg");
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "png"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: 1900px 1000px;
         }}
         </style>
         """,
         unsafe_allow_html=True 
     )# background-size: 1200px 1000px;https://developer.mozilla.org/fr/docs/Web/CSS/background-size


def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )




@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

#%% fonctions graphiques

def make_jauge(val = 328,
               previous_val = 400,
               objective_value = 370,
               max_value = 500,
               titre = "Speed",
               half = False,
              ):
    
    color_bande1 = "rgb(250, 248, 222)"
    color_bande2 = "rgb(156, 230, 66)"
    color_bande3 = "rgb(142, 210, 61)"
    color_bande4 = "rgb(126, 186, 54)"

    color_delta = 'black'#'rgb(104, 168, 32)'
    tickcolor = "darkblue"
    color_bar = "rgb(128, 111, 3)"#"rgb(86, 198, 233)"
    color_back = "white"
    color_seuil = 'blue'
    color_font = "rgb(128,111,3)"
    paper_bgcolor = "rgba(220, 219, 211,0.5)"
    
    title_size = 24
    
    if half == True:
        title_size = 15
        


    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = val,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': titre, 'font': {'size': title_size}},
        delta = {'reference': previous_val, 'increasing': {'color': color_delta}},
        gauge = {
            'axis': {'range': [None, max_value], 'tickwidth': 0.5, 'tickcolor': tickcolor},
            'bar': {'color': color_bar},
            'bgcolor': color_back,
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, (max_value)/4], 'color': color_bande1},
                {'range': [(max_value)/4, (max_value)/2], 'color': color_bande2},
                {'range': [(max_value)/2, 3*(max_value)/4], 'color': color_bande3},
                {'range': [3*(max_value)/4, max_value], 'color': color_bande4}],
            'threshold': {
                'line': {'color': "rgb(128,111,3)", 'width': 10},
                'thickness': 0.90,
                'value': objective_value}}))

    fig.update_layout(paper_bgcolor = paper_bgcolor, font = {'color': "rgb(5, 70, 40)", 'family': "Arial"})
    
    if half == True:
        fig.update_layout(
        autosize=False,
        width=230,
        height=230,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=10,
            pad=0
        ),
        paper_bgcolor = "rgba(220, 219, 211,0)")
        fig.update_yaxes(automargin=True)
    
    
    return fig


def budget(x=['ca','bu','rt'],
           y=[10,25,28] ):
    sns.set_theme()
    fig, ax = plt.subplots(figsize=(10,6), dpi=250, facecolor=(1, 1, 1, 0.8))
    sns.barplot(x=x, y=y, palette="pastel" )

    # Les différentes semaines sont données en légende
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01),
              fancybox=True, shadow=False, ncol=3)

    # Les volumes sont écrits en bleu en haut d'une barre, lorsque la valeur
    # est positive et en bas d'une barre lorsque la valeur est négative.
    for p in ax.patches:
        text = " "+format(p.get_height(), '.1f')+" "
        x = p.get_x() + p.get_width() / 2.
        y = p.get_height()
        ax.annotate(text, (x,y), ha='center', va='bottom', size=8, 
                        color='blue', xytext=(0,1), textcoords='offset points',
                        rotation=0)

    plt.xticks(rotation=45)
    plt.ylabel('Euros')
    plt.yticks(rotation=45)
    return fig




def introduction():
    txt_1 = """
            À travers le menu de navigation l'utilisateur peut accéder aux indicateurs suivants' : 
                
                - Transversalité de nos actions et rôle managerial
                - Prisme tourisme durable
                - Générateur d'activité pour nos adhérents
                - Stratégie d'influence de l'OTCP
                - Satisfaction clients
                - Pilotage budgétaire
            """

    st.title("Indicateurs OCTP 2022")
    st.text(txt_1)
        





def interface():
    data_transversalite = pd.read_excel('indicateurs.ods',
                                        engine='odf',  
                                        sheet_name="Transversalité")
    data_transversalite = data_transversalite.set_index('Unnamed: 0')

    
    data_prisme = pd.read_excel('indicateurs.ods',
                                        engine='odf',  
                                        sheet_name="Prisme tourisme durable")
    data_prisme = data_prisme.set_index('Unnamed: 0')
    
    data_b2c = pd.read_excel('indicateurs.ods',
                                        engine='odf',  
                                        sheet_name="Générateur d'activité B to C")
    data_b2c = data_b2c.set_index('Unnamed: 0')
    
    
    data_b2b = pd.read_excel('indicateurs.ods',
                                        engine='odf',  
                                        sheet_name="Générateur d'activité B to B")
    data_b2b = data_b2b.set_index('Unnamed: 0')
    
    data_octp = pd.read_excel('indicateurs.ods',
                                        engine='odf',  
                                        sheet_name="Stratégie d'influence de l'OTCP")
    data_octp = data_octp.set_index('Unnamed: 0')
    
    data_client = pd.read_excel('indicateurs.ods',
                                        engine='odf',  
                                        sheet_name="Satisfaction clients")
    data_client = data_client.set_index('Unnamed: 0')
    
    data_budget = pd.read_excel('indicateurs.ods',
                                        engine='odf',  
                                        sheet_name="Pilotage budgétaire")
    data_budget = data_budget.set_index('Unnamed: 0')
    
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    #sidebar_bg('téléchargement.jpg')
    set_bg_hack('back2.jpg')
    
    st.sidebar.image("full.png", 
                     use_column_width=True)
    
    if st.sidebar.checkbox("Présentation", value=True):
        introduction()
   
    # Sélection du type d'analyse générale à effectuer
    types_analyse = {"Actions et rôle managerial": 'test1',
                     "Prisme tourisme durable": 'test2',
                     "Activité pour nos adhérents": 'test3',
                     "Stratégie d'influence de l'OTCP": 'test4',
                     "Satisfaction clients": 'test5' ,
                     "Pilotage budgétaire": 'test6'}
    
    
    txt = "Types d'analyses: " 
    noms_types = list(types_analyse.keys())
    mode = st.sidebar.selectbox(txt, noms_types)
    
    
     #st.write('Sentiment:', run_sentiment_analysis(txt))
    
    #print(types_analyse)
    #st.write(data_transversalite)
    if mode == "Actions et rôle managerial":
        satisfaction_val = data_transversalite.loc['Relevé','Satisfaction']
        vision_val = data_transversalite.loc['Relevé','Vision partagée']
        Engagement_val = data_transversalite.loc['Relevé','Engagement']
        
        satisfaction_delta = data_transversalite.loc['Relevé précédent','Satisfaction']
        vision_delta = data_transversalite.loc['Relevé précédent','Vision partagée']
        Engagement_delta = data_transversalite.loc['Relevé précédent','Engagement']
        
        satisfaction_delta = satisfaction_val - satisfaction_delta
        vision_delta = vision_val - vision_delta
        Engagement_delta = Engagement_val - Engagement_delta
        
        
        st.title('Transversalité de nos actions et rôle managerial')
        st.header('Enquête interne')
            
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('**Satisfaction**')
            st.metric('' ,f"{satisfaction_val}", f"{satisfaction_delta}")
            
        with col2:
            st.markdown('**Vision partagée**')
            st.metric('' ,f"{vision_val}", f"{vision_delta}")
            
        with col3:
            st.markdown('**Engagement**')
            st.metric('' ,f"{Engagement_val}", f"{Engagement_delta}")
    
    if mode == 'Prisme tourisme durable':
        Participants_val = data_prisme.loc['Relevé','Participants']
        Engagement_val = data_prisme.loc['Relevé','Engagement GDS']
        stategie_val = data_prisme.loc['Relevé','Stratégie vélo']
        
        Participants_Objectif = data_prisme.loc['Objectif','Participants']
        Engagement_Objectif = data_prisme.loc['Objectif','Engagement GDS']
        stategie_Objectif = data_prisme.loc['Objectif','Stratégie vélo']
        
        Participants_delta = data_prisme.loc['Relevé précédent','Participants']
        Engagement_delta = data_prisme.loc['Relevé précédent','Engagement GDS']
        stategie_delta = data_prisme.loc['Relevé précédent','Stratégie vélo']
        
        #Participants_delta = satisfaction_val - satisfaction_delta
        Engagement_delta = Engagement_val - Engagement_delta
        stategie_delta = stategie_val - stategie_delta
        
        
        st.header('Participation au programme DD')
        fig = make_jauge(val = Participants_val,
                       previous_val = Participants_delta,
                       objective_value = Participants_Objectif,
                       max_value = max(Participants_Objectif,Participants_val)*1.1,
                       titre = "Nombre de participants"
                      )
        st.plotly_chart(fig)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**Engagement GDS**')
            st.metric('' ,f"{Engagement_val}", f"{Engagement_delta}")
            
        with col2:
            st.markdown('**Stratégie vélo**')
            st.metric('' ,f"{stategie_val}", f"{stategie_delta}")
        
    
    if mode == 'Activité pour nos adhérents':
        
        st.header("Générateur d'activité B to C" )
        vente_val = int(data_b2c.loc['Relevé','Vente billetterie'])
        frequentation_val = data_b2c.loc['Relevé','Fréquentation parisinfo.com']
        insta_val = data_b2c.loc['Relevé','Engagment Instagram']
        
        vente_delta = data_b2c.loc['Relevé précédent','Vente billetterie']
        frequentation_delta = data_b2c.loc['Relevé précédent','Fréquentation parisinfo.com']
        insta_delta = data_b2c.loc['Relevé précédent','Engagment Instagram']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('**Vente billetterie**')
            st.metric('' ,f"{vente_val}", f"{vente_delta}")
        
        with col2:
            st.markdown('**Fréquentation parisinfo.com**')
            st.metric('' ,f"{frequentation_val}", f"{frequentation_delta}")
       
        with col3:
            st.markdown('**Engagment Instagram**')
            st.metric('' ,f"{insta_val}", f"{insta_delta}")
            
        st.header("Générateur d'activité B to B" )
        wish_list_val = int(data_b2b.loc['Relevé','Indice wish list'])
        convention_val = data_b2b.loc['Relevé','Nombre de leads convention bureau']
        
        wish_list_delta = data_b2b.loc['Relevé précédent','Indice wish list']
        convention_delta = data_b2b.loc['Relevé précédent','Nombre de leads convention bureau']
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**Indice wish list**')
            st.metric('' ,f"{wish_list_val}", f"{wish_list_delta}")
        
        with col2:
            st.markdown('**Nombre de leads convention bureau**')
            st.metric('' ,f"{convention_val}", f"{convention_delta}")
    
    if mode == "Stratégie d'influence de l'OTCP":
        st.header("Stratégie d'influence de l'OTCP")
        
        reputation_val = data_octp.loc['Relevé','Indicateur de réputation']
       
        reputation_Objectif = data_octp.loc['Objectif','Indicateur de réputation']
      
        reputation_delta = data_octp.loc['Relevé précédent','Indicateur de réputation']
       
        fig = make_jauge(val = reputation_val,
                       previous_val = reputation_delta,
                       objective_value = reputation_Objectif,
                       max_value = max(reputation_Objectif,reputation_val)*1.1,
                       titre = "Indicateur de réputation"
                      )
        st.plotly_chart(fig)
        
    
    if mode == "Satisfaction clients":
        st.header("Satisfaction clients")
        
        crt_val = data_client.loc['Relevé','Enquête CRT']
        sav_val = data_client.loc['Relevé','Enquête SAV']
        otcp_val = data_client.loc['Relevé','Sondage Zoom utilité services OTCP']
        b2b_val = data_client.loc['Relevé','Satisfaction B to B']
        
        crt_Objectif = data_client.loc['Objectif','Enquête CRT']
        sav_Objectif = data_client.loc['Objectif','Enquête SAV']
        otcp_Objectif = data_client.loc['Objectif','Sondage Zoom utilité services OTCP']
        b2b_Objectif = data_client.loc['Relevé','Satisfaction B to B']
        
        crt_delta = data_client.loc['Relevé précédent','Enquête CRT']
        sav_delta = data_client.loc['Relevé précédent','Enquête SAV']
        otcp_delta = data_client.loc['Relevé précédent','Sondage Zoom utilité services OTCP']
        b2b_delta = data_client.loc['Relevé précédent','Satisfaction B to B']
        
        col1, col2 = st.columns(2)
        with col1:
            fig = make_jauge(val = crt_val,
                           previous_val = crt_delta,
                           objective_value = crt_Objectif,
                           max_value = 100,
                           titre = "Taux satisfaction enquête CRT",
                           half=True
                          )
            st.plotly_chart(fig)
        
        with col2:
            fig = make_jauge(val = b2b_val,
                           previous_val = b2b_delta,
                           objective_value = b2b_Objectif,
                           max_value = 100,
                           titre = "Opération B to B",
                           half=True
                          )
            st.plotly_chart(fig)
            
            
        col3, col4 = st.columns(2)
        with col3:
            fig = make_jauge(val = sav_val,
                           previous_val = sav_delta,
                           objective_value = sav_Objectif,
                           max_value = 5,
                           titre = "Enquête SAV",
                           half=True
                          )
            st.plotly_chart(fig)
            
        
        with col4:
            fig = make_jauge(val = otcp_val,
                           previous_val = otcp_delta,
                           objective_value = otcp_Objectif,
                           max_value = 5,
                           titre = "Services OTCP",
                           half=True
                          )
            st.plotly_chart(fig)
        
    if mode == "Pilotage budgétaire":
        st.header("Pilotage budgétaire")
        
        ca_val = data_budget.loc['Relevé','CA']
        dep_val = data_budget.loc['Relevé','Dépenses']
        rez_val = data_budget.loc['Relevé','Résultat']
        
        fig = budget(x=["chiffre d'affaires",
                       "Dépenses",
                       "Résultat"],
                    y=[ca_val,dep_val,rez_val])

       
        st.pyplot(fig)
            
        
        
        
        
        
        
    
        
       
         
            
     
       
        
       
            
        


interface()
