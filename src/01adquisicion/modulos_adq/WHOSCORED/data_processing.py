import pandas as pd
import scraper
from cookies import handle_cookies

def bucle_datos(lista_urls, paginas):
    tipo_tablas = ['Summary', 'Defensive', 'Offensive', 'Passing']
    tablas_anios = []
    for enlace in range(len(lista_urls)):
        tablas = []
        for i in range(len(tipo_tablas)):
            tablas.append(scraper.scrape_data_from_web(lista_urls[enlace], paginas[enlace], i, tipo_tablas))
        merged_tabla = pd.merge(tablas[0], tablas[1], on='Player', how='outer')
        merged_tabla = pd.merge(merged_tabla, tablas[2], on='Player', how='outer')
        merged_tabla = pd.merge(merged_tabla, tablas[2], on='Player', how='outer')
        tablas_anios.append(merged_tabla)
    tabla_datos_principales = pd.concat(tablas_anios, ignore_index=True)
    return tabla_datos_principales
