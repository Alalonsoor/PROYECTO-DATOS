import requests
import os
from sklearn.preprocessing import StandardScaler

def descargar_archivo_directo(id_archivo, directorio_destino, archivo_destino):
    # Construye la URL de descarga directa utilizando el ID del archivo
    url = f"https://drive.google.com/uc?export=download&id={id_archivo}"

    # Realiza la petición HTTP GET para descargar el archivo
    respuesta = requests.get(url, allow_redirects=True)

    # Comprueba que el directorio destino existe, si no, lo crea
    os.makedirs(directorio_destino, exist_ok=True)

    # Construye la ruta completa donde se guardará el archivo en local
    ruta_completa = os.path.join(directorio_destino, archivo_destino)

    # Guarda el contenido del archivo descargado en local
    with open(ruta_completa, 'wb') as archivo:
        archivo.write(respuesta.content)

    return archivo_destino, ruta_completa


def procesar_archivo_info(ruta_archivo_info):
    archivos_info = []
    with open(ruta_archivo_info, 'r') as archivo:
        for linea in archivo:
            id_archivo, nombre_archivo, directorio_destino = linea.strip().split(',')
            archivos_info.append((id_archivo, nombre_archivo, directorio_destino))
    return archivos_info

def preprocesamiento(arbol: bool, variables_X: list, lineal: bool, scaler:StandardScaler):
    # Ruta al archivo que contiene la información de los archivos a descargar
    ruta_archivo_info = "info_archivos_GDrive_test.txt"

    # Obtenemos la lista con la info de los archivos del fichero
    archivos_a_descargar = procesar_archivo_info(ruta_archivo_info)

    # Descargamos cada archivo de la lista
    for id_archivo, nombre_archivo, directorio_destino in archivos_a_descargar:
        nombre_archivo_descargado, ruta_archivo_guardado = descargar_archivo_directo(id_archivo, directorio_destino,
                                                                                     nombre_archivo)
        print(f"Archivo {nombre_archivo_descargado} guardado en: {ruta_archivo_guardado}")
    import pandas as pd

    df = pd.read_parquet(ruta_archivo_guardado, engine = "pyarrow")
    # Resetear el índice del DataFrame original
    df.reset_index(drop=True, inplace=True)
    df_original = df.copy()
    df = df.drop(['Anio', 'Player', 'id'], axis=1)
    if arbol != True:
        import pandas as pd
        df = df.drop(["Unnamed: 0", "Rating"], axis=1)
        col = ['Mins', 'Goals', 'Assists', 'Yel', 'Red', 'SpG', 'PS%', 'AerialsWon',
               'MotM', 'Tackles', 'Inter', 'Fouls', 'Offsides', 'Clear', 'DeffDrb',
               'Blocks', 'OwnG', 'KeyP', 'OffDrb', 'Fouled', 'Disp', 'UnsTch', 'AvgP',
               'Crosses', 'LongB', 'ThrB', 'Equipo', 'position', 'age', 'nationality',
               'height', 'marketValue', 'Año_natural', 'Titularidades', 'Suplencias',
               'Equipo_pos', '1_año_anterior', '2_año_anterior', '3_año_anterior',
               '4_año_anterior', '5_año_anterior']
        df = df[col]
        # Identifica todas las columnas numéricas excepto 'marketValue'
        numeric_columns = df.select_dtypes(include=['int', 'float']).columns
        numeric_columns_to_scale = numeric_columns.drop(['marketValue', 'Año_natural'])

        # DataFrame con solo las columnas numéricas que deseas escalar
        df_numeric_to_scale = df[numeric_columns_to_scale]

        # DataFrame con la columna 'marketValue' y otras columnas no numéricas
        df_exclude_market_value = df.drop(numeric_columns_to_scale, axis=1)
        df_numeric_scaled = scaler.transform(df_numeric_to_scale)

        # Convierte el array numpy a un DataFrame
        df_numeric_scaled = pd.DataFrame(df_numeric_scaled, columns=numeric_columns_to_scale)

        # Combina los DataFrames escalados y no escalados
        df = pd.concat([df_numeric_scaled, df_exclude_market_value], axis=1)

    from sklearn.preprocessing import OneHotEncoder
    import pandas as pd

    variables = ['Equipo', 'position', 'nationality']

    # Inicializar el codificador one-hot
    # Nota: A partir de sklearn 1.0, la salida por defecto es densa, por lo que no es necesario sparse=False.
    one_hot_encoder = OneHotEncoder()

    # Transformar las variables categóricas usando one-hot encoding
    # Aquí usamos .toarray() para garantizar que la salida es densa en caso de que el comportamiento predeterminado cambie.
    one_hot_encoded = one_hot_encoder.fit_transform(df[variables]).toarray()

    # Obtener los nombres de las columnas después de la codificación one-hot
    one_hot_encoded_names = one_hot_encoder.get_feature_names_out(variables)

    # Convertir la salida en un DataFrame y asignar nombres a las columnas
    one_hot_encoded_df = pd.DataFrame(one_hot_encoded, columns=one_hot_encoded_names)

    # Concatenar el DataFrame original con el DataFrame de las variables codificadas
    df = pd.concat([df, one_hot_encoded_df], axis=1)

    # Eliminar las columnas originales de las variables categóricas
    df = df.drop(variables, axis=1)
    df1 = df[df['marketValue'] < 80000000].copy()

    c = columnas_lista = ["Mins", "Goals", "Assists", "Yel", "Red", "SpG", "PS%", "AerialsWon", "MotM",
                          "Tackles", "Inter", "Fouls", "Offsides", "Clear", "DeffDrb", "Blocks", "OwnG", "KeyP", "Fouled", "OffDrb",
                          "Disp", "UnsTch", "AvgP", "Crosses", "LongB", "ThrB", "age", "height", "Titularidades", "Suplencias",
                          "Equipo_pos", "1_año_anterior", "2_año_anterior", "3_año_anterior", "4_año_anterior", "5_año_anterior",
                          "marketValue", "Año_natural", "Equipo_Athletic Bilbao", "Equipo_Atlético de Madrid", "Equipo_CA Osasuna",
                          "Equipo_Celta de Vigo", "Equipo_Cádiz CF", "Equipo_Deportivo Alavés", "Equipo_FC Barcelona", "Equipo_Getafe CF",
                          "Equipo_Girona FC", "Equipo_Granada CF", "Equipo_RCD Mallorca", "Equipo_Rayo Vallecano", "Equipo_Real Betis Balompié",
                          "Equipo_Real Madrid", "Equipo_Real Sociedad", "Equipo_Sevilla FC", "Equipo_UD Almería", "Equipo_UD Las Palmas",
                          "Equipo_Valencia CF", "Equipo_Villarreal CF", "position_Attacking Midfield", "position_Central Midfield",
                          "position_Centre-Back", "position_Centre-Forward", "position_Defensive Midfield", "position_Goalkeeper",
                          "position_Left Winger", "position_Left-Back", "position_Right Winger", "position_Right-Back", "nationality_Albania",
                          "nationality_Algeria", "nationality_Argentina", "nationality_Austria", "nationality_Belgium", "nationality_Brazil",
                          "nationality_Burkina Faso", "nationality_Cameroon", "nationality_Canada", "nationality_Cape Verde",
                          "nationality_Chile", "nationality_Colombia", "nationality_Cote d'Ivoire", "nationality_Croatia",
                          "nationality_DR Congo", "nationality_Denmark", "nationality_Dominican Republic", "nationality_England",
                          "nationality_Equatorial Guinea", "nationality_France", "nationality_Georgia", "nationality_Germany",
                          "nationality_Ghana", "nationality_Greece", "nationality_Guadeloupe", "nationality_Guinea", "nationality_Japan",
                          "nationality_Kosovo", "nationality_Mali", "nationality_Mexico", "nationality_Montenegro", "nationality_Morocco",
                          "nationality_Mozambique", "nationality_Netherlands", "nationality_Nigeria", "nationality_North Macedonia",
                          "nationality_Norway", "nationality_Paraguay", "nationality_Peru", "nationality_Poland", "nationality_Portugal",
                          "nationality_Romania", "nationality_Russia", "nationality_Scotland", "nationality_Senegal", "nationality_Serbia",
                          "nationality_Slovakia", "nationality_Slovenia", "nationality_Spain", "nationality_Suriname", "nationality_Sweden",
                          "nationality_Switzerland", "nationality_Syria", "nationality_Türkiye", "nationality_Ukraine",
                          "nationality_United States", "nationality_Uruguay", "nationality_Venezuela"]

    # Reordenar las columnas

    datos = df1[c]
    datos = datos.reset_index()
    col = datos.pop('marketValue')
    # Inserta la columna en la última posición
    datos.insert(len(datos.columns), 'marketValue', col)

    if lineal == False:
        X = datos.iloc[:, :-1]
        y = datos.iloc[:, -1]
    else:
        variables_X.append('Año_natural')
        X = datos[variables_X]
        y = datos.iloc[:, -1]
        variables_X.remove('Año_natural')
        print(variables_X)

    # Eliminar la columna 'Año_natural'
    X_test = X.drop(columns=['Año_natural'])
    y_test = y
    RANDOM_STATE = 83
    return X_test, y_test, RANDOM_STATE