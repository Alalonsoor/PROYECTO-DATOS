import selenium
import requests
import pandas as pd
posiciones = {"Porteros": "goalkeepers", "Medios": "midfields", "Delanteros": "forwards", "Defensas": "defenses"}
categorias = ["offensives", "efficiency", "deffensives", "discipline", "classics"]

total = []

for posicion in posiciones:
    dfs = []
    df_resultado = pd.DataFrame(columns=["NAME"])
    for categoria in categorias:
        path = "C:/Users/Usuario/Documents/Alvaro/Carrera/2-Segundo/Segundo Cuatrimestre/Proyecto de Datos 1/" + posicion + "/" + categoria + "_" + \
               posiciones[posicion] + ".csv"
        print(path)
        df = pd.read_csv(path, sep=",")
        dfs.append(df)

    for df in dfs:
        df_resultado = pd.merge(df_resultado, df, on="NAME", how="outer")

    df_resultado["Posicion"] = posicion
    total.append(df_resultado)
    df_resultado.to_csv("estadisticas_" + posicion + ".csv")

df_total = pd.concat(total)
print(df_total)
df_total.to_csv("Estadisticas_total_LaLiga.csv")

api_url = "http://localhost:8000"
la_liga_id = "ES1"

# Obtener los clubes de LaLiga
clubs_url = f"{api_url}/competitions/{la_liga_id}/clubs"
response_clubs = requests.get(clubs_url)
clubs_data = response_clubs.json()

df_players = pd.DataFrame()

for club in clubs_data.get("clubs", []):
    club_id = club.get("id")

    # Obtener los jugadores del club para una temporada específica (reemplaza "temporada_actual" con el valor correcto)
    players_url = f"{api_url}/clubs/{club_id}/players?season_id=2019"
    response_players = requests.get(players_url)
    players_data = response_players.json()

    # Agregar datos de jugadores al DataFrame
    df_players = df_players.append(players_data.get("players", []), ignore_index=True)
df_players.to_csv("transferMarket2019.csv")

anios = {2022,2021,2020,2019}
dfs = []
df_resultado = pd.DataFrame(columns=["name"])
for anio in anios:

    path = "C:/Users/Usuario/Documents/Alvaro/Carrera/2-Segundo/Segundo Cuatrimestre/Proyecto de Datos 1/SEGUNDA ENTREGA/DATOS TRANSFERMARKET/transferMarket"+str(anio)+".csv"
    print(path)
    df = pd.read_csv(path, sep = ",")
    df['Anio'] = anio
    dfs.append(df)
df_total = pd.concat(dfs)
df_total.to_csv("TransferMarket_completo.csv")
print(df_total)