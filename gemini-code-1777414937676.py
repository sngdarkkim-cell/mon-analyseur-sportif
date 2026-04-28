import streamlit as st
import pandas as pd
import requests

# Configuration de l'API (Utilise The Odds API - 500 requêtes gratuites/mois)
API_KEY = 'VOTRE_CLE_API' # À obtenir sur l'offre gratuite de the-odds-api.com
SPORT = 'soccer_france_ligue_1' # Exemple : Ligue 1
REGION = 'eu'

def get_odds():
    url = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGION}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erreur lors de la récupération des données.")
        return []

def calculate_value(odds, proba_estimee):
    # Formule : (Cote * Probabilité) - 1
    return (odds * proba_estimee) - 1

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Scanner de Value Bets", layout="wide")
st.title("📊 Analyseur de Paris Sportifs Gratuit")

if st.button('Actualiser les cotes'):
    data = get_odds()
    matches = []

    for game in data:
        home_team = game['home_team']
        away_team = game['away_team']
        
        for bookmaker in game['bookmakers']:
            # On prend les cotes du marché "h2h" (Victoire/Nul/Défaite)
            market = bookmaker['markets'][0]
            for outcome in market['outcomes']:
                matches.append({
                    'Match': f"{home_team} vs {away_team}",
                    'Bookmaker': bookmaker['title'],
                    'Selection': outcome['name'],
                    'Cote': outcome['price']
                })

    df = pd.DataFrame(matches)
    
    # Simulation d'une analyse (Ici, on pourrait coupler avec des stats historiques)
    st.subheader("Meilleures opportunités détectées")
    st.dataframe(df.sort_values(by='Cote', ascending=False))