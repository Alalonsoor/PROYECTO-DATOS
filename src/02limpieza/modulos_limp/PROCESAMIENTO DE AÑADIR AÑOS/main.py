import pandas as pd
from pymongo import MongoClient
import procesamiento_bd
import conexion_bd
import eliminacion_val_dup
import tratamiento_df


def main():
    # Cargar datos desde el archivo CSV
    df = conexion_bd.cargar_datos_desde_csv()

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
