#!/usr/bin/env python
# coding: utf-8

# <font size="3">Installar las bibliotecas necesarias unidecode, fuzzywuzzy para comparar la similitud entre los nombres de los distintos dataframes, python-Levenshtein, y joblib para realizar las comparaciones en paralelo y no en secuencial</font>

# In[217]:


get_ipython().system('pip install unidecode')
get_ipython().system('pip install fuzzywuzzy')
get_ipython().system('pip install python-Levenshtein')
get_ipython().system('pip install joblib')


# <font size="3">Importar la biblioteca pandas para trabajar con dataframes y leer los datos de la tabla 'TablaFinalSinDetalles' que contiene las estadisticas de los jugadores desde 2019-2023</font>

# In[218]:


import pandas as pd
datos = pd.read_csv("/Users/carloscole/Downloads/TablaFinalSinDetalles.csv", encoding = 'utf8', sep=';')


# <font size="3">La columna player contiene el nombre del jugador, el nombre del equipo, la edad y la posición
# Declaramos dos funciones para que en la columna player quedarnos solo con el nombre y crear una nueva columna equipo con el nombre del equipo en el qie juega</font>

# In[219]:


def f_equipo(x):
    return x.split('\n')[-1].split(',')[0]
    
def f_player(x):
    return x.split('\n')[1]


# In[220]:


datos['Equipo'] = datos['Player'].map(f_equipo)
datos['Player'] = datos['Player'].map(f_player)


# In[221]:


datos.keys()


# <font size="3">Ahora vamos a eliminar las columnas duplicadas y renombrar dos columnas que tienen el mismo nombre pero representan dos variables distintas</font>
# 

# In[222]:


datos.info()


# In[223]:


columnas_eliminar = ['_x','Apps_y', 'Mins_y', 'Goals_y', 'Assists_y', 'SpG_y', 'Rating_x',
                     'Rating_y', '_y', 'KeyP_y', 'PS%_y','_x.1', '_y.1', 'Rating_x.1', 'Rating_y.1',
                    'Apps_x.1','Mins_x.1', 'Apps_y.1', 'Mins_y.1', 'Assists']
datos = datos.drop(columnas_eliminar,axis=1)
datos = datos.rename(columns={'Drb_x': 'DeffDrb'})
datos = datos.rename(columns={'Drb_y': 'OffDrb'})


# In[224]:


datos.keys()


# <font size="3">Vamos a renombrar los nombres de las columnas que como estaban duplicadas automaticamente se habia añadido un _x para diferenciar las variables entoces vamos a eliminar eso</font>

# In[225]:


def quitar_x(x):
    return x.split('_')[0]


# In[226]:


datos = datos.replace('-', 0)
nuevos_nombres = dict(zip(datos.columns, map(quitar_x, datos.columns)))

# Aplicar el mapeo de nombres a través de rename
datos = datos.rename(columns=nuevos_nombres)


# <font size="3">Cargamos los datos de transfermarket</font>

# In[227]:


tf_data = pd.read_csv('/Users/carloscole/Downloads/TransferMarket_completo.csv')


# <font size="3">Vamos a modificar la variable Anio para que coincida con la de datos </font>

# In[228]:


tf_data['Anio'] = tf_data['Anio'].astype(str) + '-' + (tf_data['Anio'] + 1).astype(str)


# <font size="3">Eliminamos columnas que no nos aportan ningun tipo de información importante</font>

# In[229]:


columnas_eliminar = ['Unnamed: 0.1','Unnamed: 0', 'id', 'currentClub']
tf_data = tf_data.drop(columnas_eliminar, axis = 1)


# <font size="3">Como el propósito será la prdección del marketValue no nos interesa tene ningun valor nulo asi que eliminamos las filas que tengan marketValue a nulo</font>

# In[230]:


tf_data = tf_data.dropna(subset=['marketValue'], axis=0)


# <font size="3">Como vamos a hacer la predicción del valor de los jugadores de la temporada anterior podemos eliminar los datos de la temporada actual</font>

# In[231]:


datos = datos[datos['año'] != '2023-2024']


# <font size="3">Vamos a contar la cantidad de nombres de tf_data que no coinciden con ninguno en datos, podemos ver que hay 747 datos que perderiamos ya que no coinciden con ningun nombre en datos</font>

# In[232]:


datos.info()


# In[233]:


condicion = tf_data['name'].isin(datos['Player'])

# Filtrar tf_data con la condición
resultados = tf_data[~condicion]

# Imprimir los resultados
print(len(resultados))


# <font size="3">Esto es un grave problema porque perderíamos gran cantidad de datos. Este problema es común en el preprocesamiento de datos, así que buscando información sobre el problema, he encontrado una forma de valorar la similitud entre dos cadenas de texto. Puedes encontrar el código en 'https://github.com/ankitcoder123/Important-Python-Codes/blob/main/Faster%20Fuzzy%20Match%20between%20two%20columns/Fuzzy_match.py'. Trabaja en paralelo y guarda aquellos que tengan un 80% de coincidencia entre las dos cadenas; esto solo lo utilizaremos para los nombres que no tienen coincidencia.</font>
# 

# In[234]:



from unidecode import unidecode
from fuzzywuzzy import fuzz
from joblib import Parallel, delayed
import numpy as np

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


# <font size="3">Pero esto no es un trabajo automatico ya que no siempre que la similitud sea alta significa que sean el mismo jugador asi que en los siguientes fragmento de codigo voy analizando las coincidencias</font>

# In[235]:


resultados_filtrados_96_99 = [elemento for elemento in results if ((elemento[2] < 100) and (elemento[2] > 95))]
print(resultados_filtrados_96_99)
datos.loc[datos['Player'] == resultados_filtrados_96_99[0][0], 'Player'] = resultados_filtrados_96_99[0][1]
print(datos[datos['Player'] == resultados_filtrados_96_99[0][1]])


# In[236]:


resultados_filtrados_93_94 = [elemento for elemento in results if ((elemento[2] < 95) and (elemento[2] > 92))]
indices_a_eliminar = [24, 25]
print(resultados_filtrados_93_94)
# Utilizar slicing para eliminar los elementos correspondientes a los índices especificados
resultados_filtrados_93_94 = [elemento for i, elemento in enumerate(resultados_filtrados_93_94) if i not in indices_a_eliminar]
for resultado in resultados_filtrados_93_94:
    datos.loc[datos['Player'] == resultado[0], 'Player'] = resultado[1]


# In[237]:


resultados_filtrados_92 = [elemento for elemento in results if elemento[2] == 92]
print(resultados_filtrados_92)
for resultado in resultados_filtrados_92:
    datos.loc[datos['Player'] == resultado[0], 'Player'] = resultado[1]


# In[238]:


resultados_filtrados_91 = [elemento for elemento in results if elemento[2] == 91]
print(resultados_filtrados_91)
for resultado in resultados_filtrados_91:
    datos.loc[datos['Player'] == resultado[0], 'Player'] = resultado[1]


# In[239]:


resultados_filtrados_90 = [elemento for elemento in results if elemento[2] == 90]
print(resultados_filtrados_90)
datos.loc[datos['Player'] == resultados_filtrados_90[0][0], 'Player'] = resultados_filtrados_90[0][1]
print(datos[datos['Player'] == resultados_filtrados_90[0][1]])


# In[240]:


resultados_filtrados_89 = [elemento for elemento in results if elemento[2] == 89]
print(resultados_filtrados_89)
datos.loc[datos['Player'] == resultados_filtrados_89[-1][0], 'Player'] = resultados_filtrados_89[-1][1]
print(datos[datos['Player'] == resultados_filtrados_89[-1][1]])


# In[241]:


resultados_filtrados_88 = [elemento for elemento in results if elemento[2] == 88]
print(resultados_filtrados_88)
datos.loc[datos['Player'] == resultados_filtrados_88[3][0], 'Player'] = resultados_filtrados_88[3][1]
datos.loc[datos['Player'] == resultados_filtrados_88[6][0], 'Player'] = resultados_filtrados_88[6][1]
print(datos[datos['Player'] == resultados_filtrados_88[6][1]])


# In[242]:


resultados_filtrados_87 = [elemento for elemento in results if elemento[2] == 87]
print(resultados_filtrados_87)
datos.loc[datos['Player'] == resultados_filtrados_87[1][0], 'Player'] = resultados_filtrados_87[1][1]
print(datos[datos['Player'] == resultados_filtrados_87[1][1]])


# In[243]:


resultados_filtrados_86 = [elemento for elemento in results if elemento[2] == 86]
print(resultados_filtrados_86)
datos.loc[datos['Player'] == resultados_filtrados_86[-1][0], 'Player'] = resultados_filtrados_86[-1][1]
datos.loc[datos['Player'] == resultados_filtrados_86[-3][0], 'Player'] = resultados_filtrados_86[-3][1]
print(datos[datos['Player'] == resultados_filtrados_86[-1][1]])


# In[244]:


resultados_filtrados_83 = [elemento for elemento in results if elemento[2] == 83]
datos.loc[datos['Player'] == resultados_filtrados_83[6][0], 'Player'] = resultados_filtrados_83[6][1]
datos.loc[datos['Player'] == resultados_filtrados_83[-1][0], 'Player'] = resultados_filtrados_83[-1][1]
print(print(datos[datos['Player'] == resultados_filtrados_83[6][1]]))


# In[245]:


resultados_filtrados_82 = [elemento for elemento in results if elemento[2] == 82]
datos.loc[datos['Player'] == resultados_filtrados_82[-3][0], 'Player'] = resultados_filtrados_82[-3][1]
print(print(datos[datos['Player'] == resultados_filtrados_82[-3][1]]))


# In[246]:


datos.loc[datos['Player'] == 'Nacho', 'Player'] = 'Nacho Fernández'


# <font size="3">Después de tod este proceso de análisis podemos observar que hemos encontrado coincidencia para 112 jugadores más aunque todavia sigue habiendo 635 datos que no coinciden ya sea porque la escrituta de los nombres en los dos dataframes es muy distinta o porque directamente no están</font>

# In[247]:


condicion = tf_data['name'].isin(datos['Player'])

# Filtrar tf_data con la condición
resultados = tf_data[~condicion]
resultados.to_csv('No_encontrados.csv')
# Imprimir los resultados
print(len(resultados))


# In[248]:


datos.info()


# <font size="3">Juntamos los dataframes en uno por el nombre del jugador</font>

# In[249]:


df_concatenado = pd.merge(datos, tf_data, left_on=['Player', 'año'], right_on=['name', 'Anio'], how='left')
print(df_concatenado)


# In[250]:


df_concatenado.keys()


# In[251]:


df_concatenado.info()


# In[252]:


df_concatenado[df_concatenado['Player'] == 'Nacho Fernández']


# In[253]:


df_concatenado.info()


# <font size="3">Eliminamos las filas que tienen valores nulos en la columna MarketValue ya que es imprescindible para la predicción, tabmien eliminamos la dos columnas que al juntar los dataframes se repiten que son año y el nombre del jugador</font>

# In[254]:


df_concatenado = df_concatenado.dropna(subset=['marketValue'], axis=0)
df_concatenado = df_concatenado.drop(['name','Anio'],axis = 1)
df_concatenado.info()


# In[255]:


df_concatenado


# <font size="3">Transformamos la columna apariciones en dos ciolumnas distintas que contendrán las titularidades y las suplencias de cada jugador, y eliminaremos la columna 'apps'</font>

# In[256]:


extracted = df_concatenado['Apps'].str.extract(r'(\d+)?\((\d+)?\)')

# Asignar valores predeterminados de 0 cuando no hay paréntesis
df_concatenado['Titularidades'] = extracted[0].fillna(df_concatenado['Apps']).astype(int)
df_concatenado['Suplencias'] = extracted[1].fillna(0).astype(int)

# Eliminar la columna original 'Apps'
df_concatenado = df_concatenado.drop('Apps', axis=1)


# In[257]:


df_concatenado


# <font size="3">Definimos la función altura con el propósito de eliminar la m de mtros que acompaña a la altura y transformarlo de string a float</font>

# In[259]:


def altura(x):
    if isinstance(x, str):
        return x.split('m')[0]
    else:
        return x


# <font size="3">Definimos la función convertir_abreviaturas que lo que hace es cambiar la columna marketValue que contiene el símbolo del dolar y una m de millon o una k de mil lo convertimos a float</font>

# In[260]:


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


# In[261]:


df_concatenado


# In[262]:


df_concatenado['height'] = df_concatenado['height'].map(altura)
df_concatenado = df_concatenado.reset_index(drop=True)
df_concatenado


# In[263]:


df_concatenado.info()


# <font size="3">Transformarmos los datos de object a int o a double</font>

# In[264]:


df_concatenado[['Mins','Goals','Assists','Yel','Red','MotM','OwnG','age']] = df_concatenado[['Mins','Goals','Assists','Yel','Red','MotM','OwnG','age']].astype(int)
df_concatenado[['SpG','PS%','AerialsWon','Tackles','Inter','Fouls','Offsides','Clear','DeffDrb','Blocks','KeyP','OffDrb','Fouled','Off','Disp','UnsTch','AvgP','Crosses','LongB','ThrB']] = df_concatenado[['SpG','PS%','AerialsWon','Tackles','Inter','Fouls','Offsides','Clear','DeffDrb','Blocks','KeyP','OffDrb','Fouled','Off','Disp','UnsTch','AvgP','Crosses','LongB','ThrB']].astype(float)


# In[265]:


df_concatenado['height'] = df_concatenado['height'].str.replace(',', '.').astype(float)


# <font size="3">Eliminamos la columna pie predominante y año de naciminiento</font>

# In[266]:


df_concatenado = df_concatenado.drop(['dateOfBirth','foot'],axis=1)


# In[267]:


df_concatenado['Equipo'].unique()


# In[268]:


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

combined_data = {
    '2022-2023': data_2022_nombres,
    '2021-2022': data_2021_nombres,
    '2020-2021': data_2020_nombres,
    '2019-2020': data_2019_nombres
}


# In[269]:


df_concatenado['año'] = df_concatenado['año'].astype(str)
df_concatenado['año'].unique()


# <font size="3">Creamos una nueva variable 'Equipo_pos' que representa la posicion en la que quedo el equipo en eque jugaba un jugador un año en particular</font>

# In[270]:


df_concatenado['Equipo_pos'] = df_concatenado.apply(lambda row: combined_data[row['año']][row['Equipo']], axis=1)
df_concatenado.info()


# <font size="3">Eliminamos estasa columna ya que contienen muy pocos datos útiles</font>

# In[271]:


df_concatenado = df_concatenado.drop(['status', 'joined','joinedOn'], axis = 1)
df_concatenado.info()


# <font size="3">Convertimos la variable nationality a un string de un solo pais</font>

# In[272]:


import ast
df_concatenado['nationality'] = df_concatenado['nationality'].map(lambda x: ast.literal_eval(x)[0])
df_concatenado['nationality']


# In[273]:


df_concatenado.to_csv('Datos finales LaLiga.csv')


# In[274]:


tf_data.to_csv('Transfermarket limpio.csv')


# In[ ]:




