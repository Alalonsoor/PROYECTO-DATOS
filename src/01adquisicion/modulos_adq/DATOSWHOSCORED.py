import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from IPython.display import HTML
import time


def handle_cookies(driver):
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'css-1wc0q5e'))
        )
        element.click()
        print("Cookies handled.")
    except TimeoutException:
        print('No cookies found.')

def scrape_data_from_web(url, paginas, tabla, tipo_tablas):
    # Inicializar el navegador
    driver = webdriver.Chrome()
    driver.get(url)

    handle_cookies(driver)
    currentPage = 0
    condition = True
    data_list = []

    #Cambia de tabla si es necesario
    if tabla != 0 :
        next_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, tipo_tablas[tabla])))
        next_button.click() 

    #Todos los jugadores
    next_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'All players')))
    next_button.click()
    
    time.sleep(1)

    #Sacamos los nombres de las columnas
    table_head = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[5]/div[' + str(tabla+2) + ']/div[3]/div/table/thead'))
    )
    columnas = table_head.find_elements(By.TAG_NAME, 'th')
    columnas_nombres = [nombre.text for nombre in columnas]

    #Sacar cada pagina de la tabla
    while currentPage < paginas:
                # Esperar hasta que la tabla y sus elementos estén presentes en la página
                table_body = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[5]/div[' + str(tabla+2) + ']/div[3]/div/table/tbody'))
                )

                
                # Obtener todas las filas de la tabla
                rows = table_body.find_elements(By.TAG_NAME, 'tr')

                # Iterar sobre las filas e imprimir los datos
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, 'td')
                    row_data = [cell.text for cell in cells]
                    print(row_data)
                    data_list.append(row_data)

                # Intentar hacer clic en el botón de siguiente página
                driver.execute_script("window.scrollBy(0, 750)")  # Ajusta el valor según sea necesario

                # Ahora intenta hacer clic en el botón "Next" de nuevo
 
                next_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[5]/div[' + str(tabla + 2) + ']/div[4]/div/dl[2]/dd[3]/a')))
                next_button.click()
                currentPage = currentPage + 1
                print(f"Clicked next button to page {currentPage + 1}")
                time.sleep(1)  # Espera para que la página se cargue, ajusta según sea necesario
                

    
    df = pd.DataFrame(data_list, columns = columnas_nombres)
    print(df)
    return df

#Debemos pasarles la lista de las paginas: no son faciles de acceder desde una url base
def bucle_datos(lista_urls, paginas):
    tipo_tablas = ['Summary', 'Defensive', 'Offensive', 'Passing']
    tablas = []
    tablas_anios = []
    for enlace in range(len(lista_urls)):
        tablas = []
        for i in range(len(tipo_tablas))
            tablas.append(scrape_data_from_web(lista_urls[enlace], paginas[enlace], tipo_tablas[i], tipo_tablas))
        merged_tabla = pd.merge(tablas[0], tablas[1], on= 'Player', how = 'outer')
        merged_tabla = pd.merge(merged_tabla, tablas[2], on= 'Player', how = 'outer')
        merged_tabla = pd.merge(merged_tabla, tablas[2], on= 'Player', how = 'outer')
        tablas_anios.append(merged_tabla)
    tabla_datos_principales = pd.concat(tablas_anios, ignore_index=True)
    return tabla_datos_principales

lista_urls = ['https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/7889/Stages/17702/PlayerStatistics/Spain-LaLiga-2019-2020'
           'https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/8321/Stages/18851/PlayerStatistics/Spain-LaLiga-2020-2021',
           'https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/8681/Stages/19895/PlayerStatistics/Spain-LaLiga-2021-2022', 
           'https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/9149/Stages/21073/PlayerStatistics/Spain-LaLiga-2022-2023', 
           'https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/9682/Stages/22176/PlayerStatistics/Spain-LaLiga-2023-2024']
paginas = [57, 59, 61, 58, 57]
df_final_sin_detalles = bucle_datos(lista_urls, paginas)
df_final_sin_detalles.to_csv('ruta.csv', index=True, encoding='utf-8', sep = ';',)

