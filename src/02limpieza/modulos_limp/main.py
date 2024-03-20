from preprocessing import preprocess_data

def main():
    # Instalar las bibliotecas necesarias: unidecode, fuzzywuzzy, python-Levenshtein y joblib

    # Leer los datos de la tabla 'TablaFinalSinDetalles' que contiene las estadísticas de los jugadores desde 2019-2023
    datos = pd.read_csv("TablaFinalSinDetalles.csv", encoding='utf8', sep=';')
    preprocess_data(datos)

if __name__ == "__main__":
    main()
