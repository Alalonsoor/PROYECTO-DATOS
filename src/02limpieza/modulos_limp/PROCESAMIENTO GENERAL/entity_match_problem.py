import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import fuzz
from joblib import Parallel, delayed
import numpy as np
import ast

def entity_match_problem(datos,tf_data):
  # Vamos a contar la cantidad de nombres de tf_data que no coinciden con ninguno en datos, podemos ver que hay 747 datos que perderiamos ya que no coinciden con ningun nombre en datos
  condicion = tf_data['name'].isin(datos['Player'])
  
  # Filtrar tf_data con la condición
  resultados = tf_data[~condicion]
  
  # Imprimir los resultados
  print(len(resultados))
  
  # Esto es un grave problema porque perderíamos gran cantidad de datos. Este problema es común en el preprocesamiento de datos, así que buscando información sobre el problema, he encontrado una forma de valorar la similitud entre dos cadenas de texto. Puedes encontrar el código en 'https://github.com/ankitcoder123/Important-Python-Codes/blob/main/Faster%20Fuzzy%20Match%20between%20two%20columns/Fuzzy_match.py'. Trabaja en paralelo y guarda aquellos que tengan un 80% de coincidencia entre las dos cadenas; esto solo lo utilizaremos para los nombres que no tienen coincidencia.

  ca = np.array(datos["Player"])
  cb = np.array(resultados['name'])
  
  # Umbral para la comparación de similitud
  thresh = 60  # Ajusta según tus necesidades
  
  # Función para comparar en paralelo
  def parallel_fuzzy_match(idx1, idx2):
      player_a = ca[idx1]
      player_b = cb[idx2]
      similarity_ratio = fuzz.ratio(unidecode(player_a), unidecode(player_b))
      if similarity_ratio > thresh:
          team_a = datos.loc[idx1, 'Equipo']
          team_b = tf_data.loc[idx2, 'Equipo']
          if team_a == team_b:
              return [player_a, player_b, similarity_ratio]
      return [] 
  
  # Parallel Code
  results = Parallel(n_jobs=-1, verbose=1)(
      delayed(parallel_fuzzy_match)(idx1, idx2)
      for idx1 in range(len(ca))
      for idx2 in range(len(cb))
  )
  
  results = [result for sublist in results for result in sublist if result]

  resultados_formateados = []
  
  # Iterar sobre los resultados en pasos de 3 para agrupar cada par de nombres y puntuación
  for i in range(0, len(results), 3):
      nombre_1 = results[i]
      nombre_2 = results[i + 1]
      puntuacion = results[i + 2]
      resultados_formateados.append([nombre_1, nombre_2, puntuacion])
  
  resultados_formateados
  results = resultados_formateados
  # Pero esto no es un trabajo automatico ya que no siempre que la similitud sea alta significa que sean el mismo jugador asi que en los siguientes fragmento de codigo voy analizando las coincidencias
  
  resultados_100 = [elemento for elemento in results if elemento[2] == 100]
  print(resultados_100)
  datos.loc[datos['Player'] == resultados_100[0][0], 'Player'] = resultados_100[0][1]

  resultados_filtrados_89_99 = [elemento for elemento in results if ((elemento[2] < 100) and (elemento[2] > 88))]
  print(resultados_filtrados_89_99)
  datos.loc[datos['Player'] == resultados_filtrados_89_99[0][0], 'Player'] = resultados_filtrados_89_99[0][1]
  
  datos.loc[datos['Player'] == 'Nacho', 'Player'] = 'Nacho Fernández'
  
  # Después de tod este proceso de análisis podemos observar que hemos encontrado coincidencia para 112 jugadores más aunque todavia sigue habiendo 635 datos que no coinciden ya sea porque la escrituta de los nombres en los dos dataframes es muy distinta o porque directamente no están
  condicion = tf_data['name'].isin(datos['Player'])
  
  # Imprimir los resultados
  print(len(resultados))
  return datos,tf_data
