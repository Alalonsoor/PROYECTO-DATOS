from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def handle_cookies(driver):
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'css-1wc0q5e'))
        )
        element.click()
        print("Cookies handled.")
    except TimeoutException:
        print('No cookies found.')
