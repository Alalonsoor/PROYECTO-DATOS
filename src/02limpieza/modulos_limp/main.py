from preprocessing import preprocess_data

def main():
    # Instalar las bibliotecas necesarias: unidecode, fuzzywuzzy, python-Levenshtein y joblib

    # Leer los datos de la tabla 'TablaFinalSinDetalles' que contiene las estadísticas de los jugadores desde 2019-2023
    datos = pd.read_csv("TablaFinalSinDetalles.csv", encoding='utf8', sep=';')
    
    # Preprocesamiento de los player_stats
    datos = preprocess_player_stats(datos)
    
    # Leer los datos de Transfermarket
    tf_data = pd.read_csv('TransferMarket_completo.csv')

    # Preprocesamiento de los player_stats
    tf_data = preprocess_transfermarket(tf_data)

    # Tratamos el entity match problem
    datos, tf_data = entity_match_problem(datos, tf_data)

    # Integración de datos y tf_data
    datos_integrados = pd.merge(datos, tf_data, left_on=['Player', 'año'], right_on=['name', 'Anio'], how='left')
    
    # Prepocesamiento tras la integracion sobre el dataFrame final
    datos_integrados = prepocess_final(datos_integrados)

    # Guardar los datos finales como archivo parquet
    df_concatenado.to_parquet('Datos finales LaLiga.parquet')


if __name__ == "__main__":
    main()
