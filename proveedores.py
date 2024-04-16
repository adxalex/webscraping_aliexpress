from navegador import iniciar_selenium
import time
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def seleccionar_proveedor(url):
    # Esta regex busca una palabra que está justo antes de ".com"
    match = re.search(r'([\w-]+)\.com', url)
    if match:
        return match.group(1)
    return None

def amazon(url):
    proveedor = 'amazon'
    driver = iniciar_selenium(url, proveedor)

    # Ajusta el tiempo de espera si es necesario para esperar a que la página cargue
    time.sleep(5)

    try:
        # Buscar los elementos que contienen las partes del precio
        parte_entera = driver.find_element(By.CLASS_NAME, "a-price-whole").text
        decimales = driver.find_element(By.CLASS_NAME, "a-price-fraction").text
        # Construir el precio completo
        precio = f"{parte_entera}.{decimales}"

    except NoSuchElementException as e:
        print(f"No se encontró el elemento: {e}")
        precio = "No Disponible"
    except Exception as e:
        print(f"Ocurrió un error al obtener la información: {e}")
        precio = "Error"
    # Asegúrate de cerrar el navegador después de extraer la información
    driver.quit()

    return precio

def aliexpress(url):
    proveedor = 'aliexpress'
    driver = iniciar_selenium(url, proveedor)
    # Ajusta el tiempo de espera si es necesario para esperar a que la página cargue
    time.sleep(5)
    try:
        # Buscar los elementos que contienen las partes del precio
        precio_elementos = driver.find_elements(By.CSS_SELECTOR, "div.product-price-current span[class^='es-']")
        precio_parts = [element.text for element in precio_elementos]
        # Construir el precio completo
        precio = ''.join(precio_parts)
        # Eliminar caracteres no numéricos excepto el punto decimal
        precio = re.sub(r"[^\d.]", "", precio)

    except NoSuchElementException as e:
        print(f"No se encontró el elemento: {e}")
        precio = "No Disponible"
    except Exception as e:
        print(f"Ocurrió un error al obtener la información: {e}")
        precio = "Error"
    # Asegúrate de cerrar el navegador después de extraer la información
    driver.quit()
    return precio