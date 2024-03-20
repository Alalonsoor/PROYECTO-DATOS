import pandas as pd
import estadisticas
import getData


def main():
    # Procesar estadísticas
    posiciones = {"Porteros": "goalkeepers", "Medios": "midfields", "Delanteros": "forwards", "Defensas": "defenses"}
    categorias = ["offensives", "efficiency", "deffensives", "discipline", "classics"]
    df_estadisticas = estadisticas.merge_stats(posiciones, categorias)
    df_estadisticas.to_csv("Estadisticas_total_LaLiga.csv")

    # Procesar datos del mercado de transferencias
    api_url = "http://localhost:8000"
    la_liga_id = "ES1"
    df_transfer = getData.get_transfer_data(api_url, la_liga_id)
    df_transfer.to_csv("transferMarket2019.csv")

    # Procesar datos del mercado de transferencias por año
    anios = {2022, 2021, 2020, 2019}
    dfs = []
    for anio in anios:
        path = f"C:/Users/Usuario/Documents/Alvaro/Carrera/2-Segundo/Segundo Cuatrimestre/Proyecto de Datos 1/SEGUNDA ENTREGA/DATOS TRANSFERMARKET/transferMarket{anio}.csv"
        print(path)
        df = pd.read_csv(path, sep=",")
        df['Anio'] = anio
        dfs.append(df)

    df_total = pd.concat(dfs)
    df_total.to_csv("TransferMarket_completo.csv")
    print(df_total)


if __name__ == "__main__":
    main()
