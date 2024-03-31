import pandas as pd
from pymongo import MongoClient
from procesamiento_bd import valores_años_anteriores

def conectar_a_base_de_datos():
    client = MongoClient()
    db = client.LigaEspañola
    return db

def procesar_dataframe(db, df):
    df[['1_año_anterior', '2_año_anterior', '3_año_anterior', '4_año_anterior', '5_año_anterior']] = '-'
    df = df.apply(valores_años_anteriores, axis=1, db=db)
    return df

def convertir_abreviaturas(valor):
    valor_sin_euro = valor.replace('€', '')
    if 'm' in valor:
        return round(float(valor_sin_euro.replace('m', '')) * 1000000, 2)  # Multiplicar por 1 millón
    elif 'k' in valor:
        return round(float(valor_sin_euro.replace('k', '')) * 1000, 2)  # Multiplicar por 1000
    else:
        return round(float(valor_sin_euro), 2)

def exportar_dataframe(df):
    df = df.drop('Unnamed: 0',axis=1)
    df.to_csv('Datos_la_liga_preparados_entrenamiento.csv')
    df.to_parquet('Datos_la_liga_preparados_entrenamiento.parquet')
