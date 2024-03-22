import pandas as pd
import requests

def get_transfer_data(api_url, la_liga_id):
    anios = ['2022', '2021', '2020', '2019']
    dfs = []
    for anio in anios:
        print(anio)
        clubs_url = f"{api_url}/competitions/{la_liga_id}/clubs?season_id={anio}"
        response_clubs = requests.get(clubs_url)
        clubs_data = response_clubs.json()
    
        df_players = pd.DataFrame()
    
        for club in clubs_data.get("clubs", []):
            club_id = club.get("id")
            players_url = f"{api_url}/clubs/{club_id}/players?season_id={anio}"
            response_players = requests.get(players_url)
            players_data = response_players.json()
    
            df_players = pd.DataFrame(players_data.get("players", []))
            df_players['Equipo'] = club.get('name')
            df_players['Anio'] = anio
            dfs.append(df_players)
            
    df_players = pd.concat(dfs, ignore_index=True)
    
    return df_players

