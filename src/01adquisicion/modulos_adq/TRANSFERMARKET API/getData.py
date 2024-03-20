import pandas as pd
import requests

def get_transfer_data(api_url, la_liga_id):
    clubs_url = f"{api_url}/competitions/{la_liga_id}/clubs"
    response_clubs = requests.get(clubs_url)
    clubs_data = response_clubs.json()

    df_players = pd.DataFrame()

    for club in clubs_data.get("clubs", []):
        club_id = club.get("id")
        players_url = f"{api_url}/clubs/{club_id}/players?season_id=2019"
        response_players = requests.get(players_url)
        players_data = response_players.json()

        df_players = df_players.append(players_data.get("players", []), ignore_index=True)

    return df_players

