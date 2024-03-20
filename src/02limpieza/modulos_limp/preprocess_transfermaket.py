import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import fuzz
from joblib import Parallel, delayed
import numpy as np
import ast

def preprocess_transfermaket (tf_data):
  #Vamos a modificar la variable Anio para que coincida con la de datos
  tf_data['Anio'] = tf_data['Anio'].astype(str) + '-' + (tf_data['Anio'] + 1).astype(str)
  
  #Eliminamos columnas que no nos aportan ningun tipo de información importante 
  columnas_eliminar = ['Unnamed: 0.1','Unnamed: 0', 'id', 'currentClub']
  tf_data = tf_data.drop(columnas_eliminar, axis = 1)
  
  #Como el propósito será la prdección del marketValue no nos interesa tene ningun valor nulo asi que eliminamos las filas que tengan marketValue a nulo  
  tf_data = tf_data.dropna(subset=['marketValue'], axis=0)
  
  #Como vamos a hacer la predicción del valor de los jugadores de la temporada anterior podemos eliminar los datos de la temporada actual 
  datos = datos[datos['año'] != '2023-2024']

  return tf_data
