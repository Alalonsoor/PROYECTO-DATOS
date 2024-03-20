import pandas as pd
import data_processing

def main():
    lista_urls = [
        'https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/7889/Stages/17702/PlayerStatistics/Spain-LaLiga-2019-2020',
        'https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/8321/Stages/18851/PlayerStatistics/Spain-LaLiga-2020-2021',
        'https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/8681/Stages/19895/PlayerStatistics/Spain-LaLiga-2021-2022',
        'https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/9149/Stages/21073/PlayerStatistics/Spain-LaLiga-2022-2023',
        'https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/9682/Stages/22176/PlayerStatistics/Spain-LaLiga-2023-2024'
    ]
    paginas = [57, 59, 61, 58, 57]
    df_final_sin_detalles = data_processing.bucle_datos(lista_urls, paginas)
    df_final_sin_detalles.to_csv('ruta.csv', index=True, encoding='utf-8', sep=';')

if __name__ == "__main__":
    main()
