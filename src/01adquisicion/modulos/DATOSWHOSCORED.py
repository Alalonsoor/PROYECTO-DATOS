import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from IPython.display import HTML
import time

url_base = "https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/9682/Stages/22176/PlayerStatistics/Spain-LaLiga-"
def handle_cookies(driver):
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'css-1wc0q5e'))
        )
        element.click()
        print("Cookies handled.")
    except TimeoutException:
        print('No cookies found.')


def scrape_data_from_web(url):
    # Inicializar el navegador
    driver = webdriver.Chrome()
    driver.get(url)

    handle_cookies(driver)
    currentPage = 0
    condition = True
    data_list = []

    while condition:
        # Esperar hasta que la tabla y sus elementos estén presentes en la página
        table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'top-player-stats-summary-grid'))
        )
        table_head = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'player-table-statistics-head'))
        )
        table_body = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'player-table-statistics-body'))
        )

        # Obtener todas las filas de la tabla
        rows = table_body.find_elements(By.TAG_NAME, 'tr')

        # Iterar sobre las filas e imprimir los datos
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            row_data = [cell.text for cell in cells]
            print(row_data)
            data_list.append(row_data)

        # Intentar hacer clic en el botón de siguiente página si está disponible
        driver.execute_script("window.scrollBy(0, 750)")  # Ajusta el valor según sea necesario

        # Ahora intenta hacer clic en el botón "Next" de nuevo

        try:
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'a.option.clickable#next[data-page="{currentPage + 1}"]')))
            next_button.click()
            print(f"Clicked next button to page {currentPage + 1}")
            currentPage += 1
            time.sleep(1)  # Espera para que la página se cargue, ajusta según sea necesario
        except TimeoutException:
            condition = False

    df = pd.DataFrame(data_list,
                      columns=["Jugador", "Vacio", "Apps", "Mins", "Goles", "Asistencias", "Amarillas", "Rojas",
                               "Disparos/Partido", "Acierto pases", "Duelos aereos ganados", "Hombre del partido",
                               "Rating"])
    print(df)
    return df

# Año inicial y final (añadir +1 para incluir el año final en el rango)
anio_inicial = 2009
anio_final = 2023
tablas_anios = []

# Bucle para iterar sobre los años
for anio in range(anio_inicial, anio_final + 1):
    # Construir la URL completa con el año actual
    url_actual = url_base + str(anio) + "-" + str(anio + 1)
    datos_anio = scrape_data_from_web(url)
    tablas_anios.append(datos_anio)




# Llamar a la función con la URL de la página web

df = scrape_data_from_web(
    "https://www.whoscored.com/Regions/206/Tournaments/4/Seasons/9682/Stages/22176/PlayerStatistics/Spain-LaLiga-2023-2024")
# Guardar el DataFrame como un archivo CSV
df.to_csv('datos_jugadores_liga.csv', index=False)
print("DataFrame guardado como 'datos_jugadores_liga.csv'")
# Generar un enlace de descarga
download_link = f'<a href="./datos_jugadores_liga.csv" download="datos_jugadores_liga.csv">Descargar datos como CSV</a>'

# Mostrar el enlace en el cuaderno
print(HTML(download_link))

df = df.drop(columns=['Vacio']) #Sale una columa vacia por alguna razon
print(df)