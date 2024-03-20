from preprocessing import preprocess_data

def main():
    # Instalar las bibliotecas necesarias: unidecode, fuzzywuzzy, python-Levenshtein y joblib

    # Leer los datos de la tabla 'TablaFinalSinDetalles' que contiene las estadísticas de los jugadores desde 2019-2023
    datos = pd.read_csv("TablaFinalSinDetalles.csv", encoding='utf8', sep=';')
    datos = preprocess_player_stats(datos)
    
    # Leer los datos de Transfermarket
    tf_data = pd.read_csv('TransferMarket_completo.csv')

    # Preprocesamiento adicional...

    # Guardar los datos preprocesados en archivos CSV
    datos.to_csv('DatosFinalesLaLiga.csv')
    tf_data.to_csv('TransfermarketLimpio.csv')


if __name__ == "__main__":
    main()
