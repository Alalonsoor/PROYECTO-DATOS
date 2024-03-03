import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import fuzz
from joblib import Parallel, delayed
import numpy as np


datos = pd.read_csv("/Users/carloscole/Downloads/TablaFinalSinDetalles.csv", encoding = 'utf8', sep=';')


def f_equipo(x):
    return x.split('\n')[-1].split(',')[0]


def f_player(x):
    return x.split('\n')[1]


datos['Equipo'] = datos['Player'].map(f_equipo)
datos['Player'] = datos['Player'].map(f_player)

print(datos.keys())

columnas_eliminar = ['_x','Apps_y', 'Mins_y', 'Goals_y', 'Assists_y', 'SpG_y', 'Rating_x',
                     'Rating_y', '_y', 'KeyP_y', 'PS%_y','_x.1', '_y.1', 'Rating_x.1', 'Rating_y.1',
                    'Apps_x.1','Mins_x.1', 'Apps_y.1', 'Mins_y.1', 'Assists']
datos = datos.drop(columnas_eliminar,axis=1)
datos = datos.rename(columns={'Drb_x': 'DeffDrb'})
datos = datos.rename(columns={'Drb_y': 'OffDrb'})
print(datos.keys())

def quitar_x(x):
    return x.split('_')[0]

datos = datos.replace('-', 0)
nuevos_nombres = dict(zip(datos.columns, map(quitar_x, datos.columns)))

# Aplicar el mapeo de nombres a través de rename
datos = datos.rename(columns=nuevos_nombres)


tf_data = pd.read_csv('/Users/carloscole/Downloads/TransferMarket_completo.csv')
tf_data['Anio'] = tf_data['Anio'].astype(str) + '-' + (tf_data['Anio'] + 1).astype(str)
columnas_eliminar = ['Unnamed: 0.1','Unnamed: 0', 'id', 'currentClub']
tf_data = tf_data.drop(columnas_eliminar, axis = 1)
tf_data = tf_data.dropna(subset=['marketValue'], axis=0)
datos = datos[datos['año'] != '2023-2024']

condicion = tf_data['name'].isin(datos['Player'])

# Filtrar tf_data con la condición
resultados = tf_data[~condicion]

# Imprimir los resultados
print(len(resultados))

ca = np.array(datos["Player"])
cb = np.array(resultados['name'])

# Umbral para la comparación de similitud
thresh = 80  # Ajusta según tus necesidades

# Función para comparar en paralelo
def parallel_fuzzy_match(idxa, idxb):
    return [ca[idxa], cb[idxb], fuzz.ratio(ca[idxa], cb[idxb])]

# Parallel Code
results = Parallel(n_jobs=-1, verbose=1)(
    delayed(parallel_fuzzy_match)(idx1, idx2)
    for idx1 in range(len(ca))
    for idx2 in range(len(cb))
    if fuzz.ratio(ca[idx1], cb[idx2]) > thresh
)

resultados_filtrados_96_99 = [elemento for elemento in results if ((elemento[2] < 100) and (elemento[2] > 95))]
print(resultados_filtrados_96_99)
datos.loc[datos['Player'] == resultados_filtrados_96_99[0][0], 'Player'] = resultados_filtrados_96_99[0][1]
print(datos[datos['Player'] == resultados_filtrados_96_99[0][1]])

resultados_filtrados_93_94 = [elemento for elemento in results if ((elemento[2] < 95) and (elemento[2] > 92))]
indices_a_eliminar = [24, 25]
print(resultados_filtrados_93_94)
# Utilizar slicing para eliminar los elementos correspondientes a los índices especificados
resultados_filtrados_93_94 = [elemento for i, elemento in enumerate(resultados_filtrados_94_96) if i not in indices_a_eliminar]
for resultado in resultados_filtrados_93_94:
    datos.loc[datos['Player'] == resultado[0], 'Player'] = resultado[1]

resultados_filtrados_92 = [elemento for elemento in results if elemento[2] == 92]
print(resultados_filtrados_92)
for resultado in resultados_filtrados_92:
    datos.loc[datos['Player'] == resultado[0], 'Player'] = resultado[1]


resultados_filtrados_91 = [elemento for elemento in results if elemento[2] == 91]
print(resultados_filtrados_91)
for resultado in resultados_filtrados_91:
    datos.loc[datos['Player'] == resultado[0], 'Player'] = resultado[1]


resultados_filtrados_90 = [elemento for elemento in results if elemento[2] == 90]
print(resultados_filtrados_90)
datos.loc[datos['Player'] == resultados_filtrados_90[0][0], 'Player'] = resultados_filtrados_90[0][1]
print(datos[datos['Player'] == resultados_filtrados_90[0][1]])

resultados_filtrados_89 = [elemento for elemento in results if elemento[2] == 89]
print(resultados_filtrados_89)
datos.loc[datos['Player'] == resultados_filtrados_89[-1][0], 'Player'] = resultados_filtrados_89[-1][1]
print(datos[datos['Player'] == resultados_filtrados_89[-1][1]])

resultados_filtrados_88 = [elemento for elemento in results if elemento[2] == 88]
print(resultados_filtrados_88)
datos.loc[datos['Player'] == resultados_filtrados_88[3][0], 'Player'] = resultados_filtrados_88[3][1]
datos.loc[datos['Player'] == resultados_filtrados_88[6][0], 'Player'] = resultados_filtrados_88[6][1]
print(datos[datos['Player'] == resultados_filtrados_88[6][1]])


resultados_filtrados_87 = [elemento for elemento in results if elemento[2] == 87]
print(resultados_filtrados_87)
datos.loc[datos['Player'] == resultados_filtrados_87[1][0], 'Player'] = resultados_filtrados_87[1][1]
print(datos[datos['Player'] == resultados_filtrados_87[1][1]])

resultados_filtrados_86 = [elemento for elemento in results if elemento[2] == 86]
print(resultados_filtrados_86)
datos.loc[datos['Player'] == resultados_filtrados_86[-1][0], 'Player'] = resultados_filtrados_86[-1][1]
datos.loc[datos['Player'] == resultados_filtrados_86[-3][0], 'Player'] = resultados_filtrados_86[-3][1]
print(datos[datos['Player'] == resultados_filtrados_86[-1][1]])

resultados_filtrados_83 = [elemento for elemento in results if elemento[2] == 83]
datos.loc[datos['Player'] == resultados_filtrados_83[6][0], 'Player'] = resultados_filtrados_83[6][1]
datos.loc[datos['Player'] == resultados_filtrados_83[-1][0], 'Player'] = resultados_filtrados_83[-1][1]
print(print(datos[datos['Player'] == resultados_filtrados_83[6][1]]))

resultados_filtrados_82 = [elemento for elemento in results if elemento[2] == 82]
datos.loc[datos['Player'] == resultados_filtrados_82[-3][0], 'Player'] = resultados_filtrados_82[-3][1]
print(print(datos[datos['Player'] == resultados_filtrados_82[-3][1]]))

datos.loc[datos['Player'] == 'Nacho', 'Player'] = 'Nacho Fernández'

condicion = tf_data['name'].isin(datos['Player'])

# Filtrar tf_data con la condición
resultados = tf_data[~condicion]
resultados.to_csv('No_encontrados.csv')
# Imprimir los resultados
print(len(resultados))

df_concatenado = pd.merge(datos, tf_data, left_on=['Player', 'año'], right_on=['name', 'Anio'], how='left')
print(df_concatenado)

print(df_concatenado.keys())

print(df_concatenado[df_concatenado['Player'] == 'Nacho Fernández'])


print(df_concatenado.info())

df_concatenado = df_concatenado.dropna(subset=['marketValue'], axis=0)
df_concatenado = df_concatenado.drop(['name','Anio'],axis = 1)
print(df_concatenado.info())


extracted = df_concatenado['Apps'].str.extract(r'(\d+)?\((\d+)?\)')

# Asignar valores predeterminados de 0 cuando no hay paréntesis o solo hay un número
df_concatenado['Titularidades'] = extracted[0].fillna(0)
df_concatenado['Suplencias'] = extracted[1].fillna(0)

# Convertir a enteros
df_concatenado['Titularidades'] = df_concatenado['Titularidades'].astype(int)
df_concatenado['Suplencias'] = df_concatenado['Suplencias'].astype(int)
df_concatenado = df_concatenado.drop('Apps',axis = 1)


print(df_concatenado['height'][0].split('m')[0])


def altura(x):
    if isinstance(x, str):
        return x.split('m')[0]
    else:
        return x

def convertir_abreviaturas(valor):
    valor_sin_euro = valor.replace('€', '')
    if 'm' in valor:
        return round(float(valor_sin_euro.replace('m', '')) * 1000000, 2)  # Multiplicar por 1 millón
    elif 'k' in valor:
        return round(float(valor_sin_euro.replace('k', '')) * 1000, 2)  # Multiplicar por 1000
    else:
        return round(float(valor_sin_euro), 2)

# Aplicar la función a la columna 'marketValue'
df_concatenado['marketValue'] = df_concatenado['marketValue'].apply(convertir_abreviaturas)


print(df_concatenado)

df_concatenado['height'] = df_concatenado['height'].map(altura)
df_concatenado = df_concatenado.reset_index(drop=True)
print(df_concatenado)

print(df_concatenado.info())

df_concatenado[['Mins','Goals','Assists','Yel','Red','MotM','OwnG','age']] = df_concatenado[['Mins','Goals','Assists','Yel','Red','MotM','OwnG','age']].astype(int)
df_concatenado[['SpG','PS%','AerialsWon','Tackles','Inter','Fouls','Offsides','Clear','DeffDrb','Blocks','KeyP','OffDrb','Fouled','Off','Disp','UnsTch','AvgP','Crosses','LongB','ThrB']] = df_concatenado[['SpG','PS%','AerialsWon','Tackles','Inter','Fouls','Offsides','Clear','DeffDrb','Blocks','KeyP','OffDrb','Fouled','Off','Disp','UnsTch','AvgP','Crosses','LongB','ThrB']].astype(float)


df_concatenado['height'] = df_concatenado['height'].str.replace(',', '.').astype(float)

df_concatenado = df_concatenado.drop(['dateOfBirth','foot'],axis=1)

print(df_concatenado['Equipo'].unique())

data_2022_nombres = {
    'Barcelona': 1,
    'Real Madrid': 2,
    'Atletico': 3,
    'Real Sociedad': 4,
    'Villarreal': 5,
    'Real Betis': 6,
    'Osasuna': 7,
    'Athletic Club': 8,
    'Mallorca': 9,
    'Girona': 10,
    'Sevilla': 11,
    'Rayo Vallecano': 12,
    'Celta Vigo': 13,
    'Valencia': 14,
    'Getafe': 15,
    'Cadiz': 16,
    'Almeria': 17,
    'Real Valladolid': 18,
    'Espanyol': 19,
    'Elche': 20,
    'Granada': 21,
    'Levante': 22,
    'Deportivo Alaves': 23,
    'Leganes':24,
    'SD Huesca': 25,
    'Eibar': 26,
}

data_2021_nombres = {
    'Real Madrid': 1,
    'Barcelona': 2,
    'Atletico': 3,
    'Sevilla': 4,
    'Real Betis': 5,
    'Real Sociedad': 6,
    'Villarreal': 7,
    'Athletic Club': 8,
    'Valencia': 9,
    'Osasuna': 10,
    'Celta Vigo': 11,
    'Rayo Vallecano': 12,
    'Elche': 13,
    'Espanyol': 14,
    'Getafe': 15,
    'Mallorca': 16,
    'Cadiz': 17,
    'Granada': 18,
    'Levante': 19,
    'Deportivo Alaves': 20,
    'SD Huesca': 21,
    'Real Valladolid': 22,
    'Eibar': 23,
    'Girona': 24,
    'Leganes': 25,
    'Almeria': 26
}

data_2020_nombres = {
    'Atletico': 1,
    'Real Madrid': 2,
    'Barcelona': 3,
    'Sevilla': 4,
    'Real Sociedad': 5,
    'Real Betis': 6,
    'Villarreal': 7,
    'Celta Vigo': 8,
    'Athletic Club': 9,
    'Granada': 10,
    'Osasuna': 11,
    'Cadiz': 12,
    'Valencia': 13,
    'Levante': 14,
    'Getafe': 15,
    'Deportivo Alaves': 16,
    'Elche': 17,
    'SD Huesca': 18,
    'Real Valladolid': 19,
    'Eibar': 20,
    'Leganes': 21,
    'Mallorca': 22,
    'Espanyol': 23,
    'Girona': 24,
    'Rayo Vallecano': 25,
    'Almeria': 26
}

data_2019_nombres = {
    'Real Madrid': 1,
    'Barcelona': 2,
    'Atletico': 3,
    'Sevilla': 4,
    'Villarreal': 5,
    'Real Sociedad': 6,
    'Granada': 7,
    'Getafe': 8,
    'Valencia': 9,
    'Osasuna': 10,
    'Athletic Club': 11,
    'Levante': 12,
    'Real Valladolid': 13,
    'Eibar': 14,
    'Real Betis': 15,
    'Deportivo Alaves': 16,
    'Celta Vigo': 17,
    'Leganes': 18,
    'Mallorca': 19,
    'Espanyol': 20,
    'SD Huesca': 21,
    'Cadiz': 22,
    'Rayo Vallecano': 23,
    'Girona': 24,
    'Almeria': 25,
    'Elche': 26
}

df_concatenado['equipo_2022'] = df_concatenado['Equipo'].map(data_2022_nombres)
df_concatenado['equipo_2021'] = df_concatenado['Equipo'].map(data_2021_nombres)
df_concatenado['equipo_2020'] = df_concatenado['Equipo'].map(data_2020_nombres)
df_concatenado['equipo_2019'] = df_concatenado['Equipo'].map(data_2019_nombres)
df_concatenado = df_concatenado.drop('Equipo', axis = 1)
print(df_concatenado.info())


df_concatenado.to_csv('Datos finales LaLiga.csv')


tf_data.to_csv('Transfermarket limpio.csv')