import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import fuzz
from joblib import Parallel, delayed
import numpy as np
import ast

def prepocess_final(df_concatenado):
  # Eliminamos las filas que tienen valores nulos en la columna MarketValue ya que es imprescindible para la predicción, tabmien eliminamos la dos columnas que al juntar los dataframes se repiten que son año y el nombre del jugador
  df_concatenado = df_concatenado.dropna(subset=['marketValue'], axis=0)
  df_concatenado = df_concatenado.drop(['name','Anio'],axis = 1)
  
  # Transformamos la columna apariciones en dos ciolumnas distintas que contendrán las titularidades y las suplencias de cada jugador, y eliminaremos la columna 'apps'
  extracted = df_concatenado['Apps'].str.extract(r'(\d+)?\((\d+)?\)')
  
  # Asignar valores predeterminados de 0 cuando no hay paréntesis
  df_concatenado['Titularidades'] = extracted[0].fillna(df_concatenado['Apps']).astype(int)
  df_concatenado['Suplencias'] = extracted[1].fillna(0).astype(int)
  
  # Eliminar la columna original 'Apps'
  df_concatenado = df_concatenado.drop('Apps', axis=1)
  
  # Definimos la función altura con el propósito de eliminar la m de mtros que acompaña a la altura y transformarlo de string a float
  
  def altura(x):
      if isinstance(x, str):
          return x.split('m')[0]
      else:
          return x
  
  # Definimos la función convertir_abreviaturas que lo que hace es cambiar la columna marketValue que contiene el símbolo del dolar y una m de millon o una k de mil lo convertimos a float
  
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
  df_concatenado['height'] = df_concatenado['height'].map(altura)
  df_concatenado = df_concatenado.reset_index(drop=True)
  
  # Transformarmos los datos de object a int o a double
  
  df_concatenado[['Mins','Goals','Assists','Yel','Red','MotM','OwnG','age']] = df_concatenado[['Mins','Goals','Assists','Yel','Red','MotM','OwnG','age']].astype(int)
  df_concatenado[['SpG','PS%','AerialsWon','Tackles','Inter','Fouls','Offsides','Clear','DeffDrb','Blocks','KeyP','OffDrb','Fouled','Off','Disp','UnsTch','AvgP','Crosses','LongB','ThrB']] = df_concatenado[['SpG','PS%','AerialsWon','Tackles','Inter','Fouls','Offsides','Clear','DeffDrb','Blocks','KeyP','OffDrb','Fouled','Off','Disp','UnsTch','AvgP','Crosses','LongB','ThrB']].astype(float)
  df_concatenado['height'] = df_concatenado['height'].str.replace(',', '.').astype(float)
  
  # Eliminamos la columna pie predominante y año de naciminiento
  
  df_concatenado = df_concatenado.drop(['dateOfBirth','foot'],axis=1)
  
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
  
  def aplicar_mapeo(diccionario, mapeo):
    return {mapeo.get(key, key): value for key, value in diccionario.items()}

  # Aplicar el mapeo a cada diccionario de datos
  data_2022_nombres_mapped = aplicar_mapeo(data_2022_nombres, equipo_mapping_inverse)
  data_2021_nombres_mapped = aplicar_mapeo(data_2021_nombres, equipo_mapping_inverse)
  data_2020_nombres_mapped = aplicar_mapeo(data_2020_nombres, equipo_mapping_inverse)
  data_2019_nombres_mapped = aplicar_mapeo(data_2019_nombres, equipo_mapping_inverse)
  
  combined_data_mapped = {
      '2022-2023': data_2022_nombres_mapped,
      '2021-2022': data_2021_nombres_mapped,
      '2020-2021': data_2020_nombres_mapped,
      '2019-2020': data_2019_nombres_mapped
  }
  
  df_concatenado['año'] = df_concatenado['año'].astype(str)

  df_concatenado = df_concatenado.drop('Equipo_y', axis=1)
  df_concatenado = df_concatenado.rename(columns={'Equipo_x': 'Equipo'})
  
  # Creamos una nueva variable 'Equipo_pos' que representa la posicion en la que quedo el equipo en eque jugaba un jugador un año en particular  
  df_concatenado['Equipo_pos'] = df_concatenado.apply(lambda row: combined_data[row['año']][row['Equipo']], axis=1)
  
  # Eliminamos estasa columna ya que contienen muy pocos datos útiles
  df_concatenado = df_concatenado.drop(['status', 'joined','joinedOn','signedFrom'], axis = 1)

  mean_height = np.mean(df_concatenado['height'])
  df_concatenado['height'].fillna(mean_height, inplace=True)
  
  # Convertimos la variable nationality a un string de un solo pais
  df_concatenado['nationality'] = df_concatenado['nationality'].map(lambda x: ast.literal_eval(x)[0])
