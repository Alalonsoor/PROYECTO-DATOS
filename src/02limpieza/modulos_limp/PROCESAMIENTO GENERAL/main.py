import preprocess_transfermarket
import prepocess_final
import preprocess_player_stats
import entity_match_problem
import pandas as pd
import cargarGDrive
def main():

    # Instalar las bibliotecas necesarias: unidecode, fuzzywuzzy, python-Levenshtein y joblib
    ruta_archivo_info = "info_archivos_GDrive.txt"

    # Obtenemos la lista con la info de los archivos del fichero
    archivos_a_descargar = cargarGDrive.procesar_archivo_info(ruta_archivo_info)

    # Descargamos cada archivo de la lista
    for id_archivo, nombre_archivo, directorio_destino in archivos_a_descargar:
        nombre_archivo_descargado, ruta_archivo_guardado = cargarGDrive.descargar_archivo_directo(id_archivo,
                                                                                                  directorio_destino,
                                                                                             nombre_archivo)
        if(nombre_archivo_descargado == "DATOS WHOSCORED.csv"):
            ruta_who = ruta_archivo_guardado
        else:
            ruta_transfer = ruta_archivo_guardado
        print(f"Archivo {nombre_archivo_descargado} guardado en: {ruta_archivo_guardado}")
    # Leer los datos de la tabla 'TablaFinalSinDetalles' que contiene las estadísticas de los jugadores desde 2019-2023
    datos = pd.read_csv(ruta_who, encoding='utf8', sep=';')
    
    # Preprocesamiento de los player_stats
    datos = preprocess_player_stats(datos)
    
    # Leer los datos de Transfermarket
    tf_data = pd.read_csv(ruta_transfer)

    # Preprocesamiento de los player_stats
    tf_data = preprocess_transfermarket(tf_data)

    # Tratamos el entity match problem
    datos, tf_data = entity_match_problem(datos, tf_data)

    # Integración de datos y tf_data
    datos_integrados = pd.merge(datos, tf_data, left_on=['Player', 'año'], right_on=['name', 'Anio'], how='left')
    
    # Prepocesamiento tras la integracion sobre el dataFrame final
    datos_integrados = prepocess_final(datos_integrados)

    # Guardar los datos finales como archivo parquet
    datos_integrados.to_parquet('Datos finales LaLiga.parquet')


if __name__ == "__main__":
    main()
