import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from cookies import handle_cookies

def scrape_data_from_web(url, paginas, tabla, tipo_tablas):
    # Inicializar el navegador
    driver = webdriver.Chrome()
    driver.get(url)

    handle_cookies(driver)
    currentPage = 0
    data_list = []

    # Cambia de tabla si es necesario
    if tabla != 0:
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, tipo_tablas[tabla]))
        )
        next_button.click()

    # Todos los jugadores
    next_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'All players'))
    )
    next_button.click()

    time.sleep(1)

    # Sacamos los nombres de las columnas
    table_head = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[5]/div[' + str(tabla+2) + ']/div[3]/div/table/thead'))
    )
    columnas = table_head.find_elements(By.TAG_NAME, 'th')
    columnas_nombres = [nombre.text for nombre in columnas]

    # Sacar cada pagina de la tabla
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
            data_list.append(row_data)

        # Intentar hacer clic en el botón de siguiente página
        driver.execute_script("window.scrollBy(0, 750)")  # Ajusta el valor según sea necesario

        # Ahora intenta hacer clic en el botón "Next" de nuevo
        next_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[5]/div[' + str(tabla + 2) + ']/div[4]/div/dl[2]/dd[3]/a'))
        )
        next_button.click()
        currentPage = currentPage + 1
        print(f"Clicked next button to page {currentPage + 1}")
        time.sleep(1)  # Espera para que la página se cargue, ajusta según sea necesario

    df = pd.DataFrame(data_list, columns=columnas_nombres)
    print(df)
    return df
