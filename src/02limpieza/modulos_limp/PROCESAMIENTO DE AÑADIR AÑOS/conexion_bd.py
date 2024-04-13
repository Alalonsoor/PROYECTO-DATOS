import pandas as pd
from pymongo import MongoClient


def cargar_datos_desde_csv(path):
    df = pd.read_csv(path)
    df.set_index('id', inplace=True)
    return df

def conectar_a_base_de_datos():
    client = MongoClient()
    db = client.LigaEspañola
    return db

def buscar_por_id(db):
    resultados = db.Futbolistas.find({'id': '668179'})
    for resultado in resultados:
        print(resultado)

def buscar_valor_por_fecha(db):
    meses = ['Jun', 'Jul', 'Aug', 'May', 'Apr', 'Mar', 'Oct', 'Feb', 'Nov', 'Jan', 'Dec']
    encontrado = False
    i = 0

    while not encontrado:
        s = meses[i] + r'\s\d{1,2},\s2018'
        resultados = db.Futbolistas.find(
            {
                'id': '28003',
                'marketValueHistory.date': {'$regex': s}
            },
            {'marketValueHistory.$': 1, '_id': 0}
        )
        i += 1

        for resultado in resultados:
            valor = resultado['marketValueHistory'][0]['value']
            print(valor)
            encontrado = True