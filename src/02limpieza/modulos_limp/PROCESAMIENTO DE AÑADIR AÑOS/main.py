import conexion_bd
import eliminacion_val_dup
import tratamiento_df
import cargarGDrive

def main():
    # Ruta al archivo que contiene la información de los archivos a descargar
    ruta_archivo_info = "info_archivos_GDrive.txt"

    # Obtenemos la lista con la info de los archivos del fichero
    archivos_a_descargar = cargarGDrive.procesar_archivo_info(ruta_archivo_info)

    # Descargamos cada archivo de la lista
    for id_archivo, nombre_archivo, directorio_destino in archivos_a_descargar:
        nombre_archivo_descargado, ruta_archivo_guardado = cargarGDrive.descargar_archivo_directo(id_archivo, directorio_destino,
                                                                                                  nombre_archivo)
        print(f"Archivo {nombre_archivo_descargado} guardado en: {ruta_archivo_guardado}")

    # Cargar datos desde el archivo CSV
    df = conexion_bd.cargar_datos_desde_csv(ruta_archivo_guardado)

    # Conectar a la base de datos
    db = conexion_bd.conectar_a_base_de_datos()

    # Buscar por ID
    conexion_bd.buscar_por_id(db)

    # Buscar valor por fecha
    conexion_bd.buscar_valor_por_fecha(db)

    # Eliminar valores duplicados
    eliminacion_val_dup.eliminar_valores_duplicados(db)

    # Procesar DataFrame
    df = tratamiento_df.procesar_dataframe(db, df)

    # Convertir abreviaturas
    df['1_año_anterior'] = df['1_año_anterior'].apply(tratamiento_df.convertir_abreviaturas)
    df['2_año_anterior'] = df['2_año_anterior'].apply(tratamiento_df.convertir_abreviaturas)
    df['3_año_anterior'] = df['3_año_anterior'].apply(tratamiento_df.convertir_abreviaturas)
    df['4_año_anterior'] = df['4_año_anterior'].apply(tratamiento_df.convertir_abreviaturas)
    df['5_año_anterior'] = df['5_año_anterior'].apply(tratamiento_df.convertir_abreviaturas)

    # Exportar DataFrame
    tratamiento_df.exportar_dataframe(df)


if __name__ == "__main__":
    main()
