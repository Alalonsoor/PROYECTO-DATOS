import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import fuzz
from joblib import Parallel, delayed
import numpy as np
import ast

def preprocess_player_stats(datos):

    # Función para extraer el nombre del equipo
    def f_equipo(x):
        return x.split('\n')[-1].split(',')[0]

    # Función para extraer el nombre del jugador
    def f_player(x):
        return x.split('\n')[1]

    datos['Equipo'] = datos['Player'].map(f_equipo)
    datos['Player'] = datos['Player'].map(f_player)

    # Eliminar columnas duplicadas y renombrar columnas
    columnas_eliminar = ['_x','Apps_y', 'Mins_y', 'Goals_y', 'Assists_y', 'SpG_y', 'Rating_x',
                        'Rating_y', '_y', 'KeyP_y', 'PS%_y','_x.1', '_y.1', 'Rating_x.1', 'Rating_y.1',
                        'Apps_x.1','Mins_x.1', 'Apps_y.1', 'Mins_y.1', 'Assists']
    datos = datos.drop(columnas_eliminar,axis=1)
    datos = datos.rename(columns={'Drb_x': 'DeffDrb'})
    datos = datos.rename(columns={'Drb_y': 'OffDrb'})

    # Renombrar nombres de columnas
    def quitar_x(x):
        return x.split('_')[0]

    datos = datos.replace('-', 0)
    nuevos_nombres = dict(zip(datos.columns, map(quitar_x, datos.columns)))
    datos = datos.rename(columns=nuevos_nombres)

    
