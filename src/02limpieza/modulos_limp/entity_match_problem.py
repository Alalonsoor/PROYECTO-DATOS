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
  
  # Pero esto no es un trabajo automatico ya que no siempre que la similitud sea alta significa que sean el mismo jugador asi que en los siguientes fragmento de codigo voy analizando las coincidencias
  
  resultados_filtrados_96_99 = [elemento for elemento in results if ((elemento[2] < 100) and (elemento[2] > 95))]
  print(resultados_filtrados_96_99)
  datos.loc[datos['Player'] == resultados_filtrados_96_99[0][0], 'Player'] = resultados_filtrados_96_99[0][1]
  print(datos[datos['Player'] == resultados_filtrados_96_99[0][1]])
  
  
  resultados_filtrados_93_94 = [elemento for elemento in results if ((elemento[2] < 95) and (elemento[2] > 92))]
  indices_a_eliminar = [24, 25]
  print(resultados_filtrados_93_94)
  # Utilizar slicing para eliminar los elementos correspondientes a los índices especificados
  resultados_filtrados_93_94 = [elemento for i, elemento in enumerate(resultados_filtrados_93_94) if i not in indices_a_eliminar]
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
  
  # Después de tod este proceso de análisis podemos observar que hemos encontrado coincidencia para 112 jugadores más aunque todavia sigue habiendo 635 datos que no coinciden ya sea porque la escrituta de los nombres en los dos dataframes es muy distinta o porque directamente no están
  condicion = tf_data['name'].isin(datos['Player'])
  
  # Imprimir los resultados
  print(len(resultados))
  return datos,tf_data
