import pandas as pd

def merge_stats(posiciones, categorias):
    total = []
    for posicion in posiciones:
        dfs = []
        df_resultado = pd.DataFrame(columns=["NAME"])
        for categoria in categorias:
            path = f"C:/Users/Usuario/Documents/Alvaro/Carrera/2-Segundo/Segundo Cuatrimestre/Proyecto de Datos 1/{posicion}/{categoria}_{posiciones[posicion]}.csv"
            df = pd.read_csv(path, sep=",")
            dfs.append(df)

        for df in dfs:
            df_resultado = pd.merge(df_resultado, df, on="NAME", how="outer")

        df_resultado["Posicion"] = posicion
        total.append(df_resultado)
        df_resultado.to_csv("estadisticas_" + posicion + ".csv")

    df_total = pd.concat(total)
    return df_total

