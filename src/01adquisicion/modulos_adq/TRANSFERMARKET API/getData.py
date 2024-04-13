import pandas as pd
import requests
from pymongo import MongoClient


def get_transfer_data(api_url, la_liga_id):
    

    # Crear una conexión con una "base de datos" en memoria
    client = MongoClient()
    db = client.LigaEspañola
    
    
    anios = ['2022', '2021', '2020', '2019']
    dfs = []
    for anio in anios:
        clubs_url = f"{api_url}/competitions/{la_liga_id}/clubs?season_id={anio}"
        response_clubs = requests.get(clubs_url)
        clubs_data = response_clubs.json()
    
        df_players = pd.DataFrame()
    
        for club in clubs_data.get("clubs", []):
            club_id = club.get("id")
            players_url = f"{api_url}/clubs/{club_id}/players?season_id={anio}"
            response_players = requests.get(players_url)
            players_data = response_players.json()
            
            for player in players_data.get("players", []):
                player_id = player.get('id')          
                market_value_pasado_url = f"{api_url}/players/{player_id}/market_value"
                response_market_value_pasado = requests.get(market_value_pasado_url)
                market_value_pasado_data = response_market_value_pasado.json()
                db.Futbolistas.insert_one(market_value_pasado_data)
            
            df_players = pd.DataFrame(players_data.get("players", []))
            df_players['Equipo'] = club.get('name')
            df_players['Anio'] = anio
            dfs.append(df_players)

    df_players = pd.concat(dfs, ignore_index=True)
    df_players.to_csv("TransferMarket2.csv")
    
    return df_players

