import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración inicial
CHROMEDRIVER_PATH = 'ruta/chromedriver.exe'  # Asegúrate de que es la ruta completa y correcta
SITE_URL = 'https://ds.aliexpress.com/#/hot-search?title=Winning%20Products'

# Añadir chromedriver al PATH
os.environ["PATH"] += os.pathsep + os.path.dirname(CHROMEDRIVER_PATH)

chrome_options = Options()
browser = webdriver.Chrome(options=chrome_options)

browser.get(SITE_URL)

wait = WebDriverWait(browser, 10)

product_links_js = browser.execute_script("return document.querySelectorAll('a.cardWrap--RpEaA2WG');")

# Guardar los enlaces de los dos primeros productos en variables
product_link_1 = product_links_js[0].get_attribute('href')
product_link_2 = product_links_js[1].get_attribute('href')

# Cerrar el navegador
browser.quit()

# Abrir de nuevo el navegador
browser = webdriver.Chrome(options=chrome_options)

# Navegamos hacia el contenido de product_link_1
browser.get(product_link_1)

input("wait")

# Esperar a que el elemento reviewer--wrap--sPGWrNq esté presente en la página
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "reviewer--wrap--sPGWrNq")))

# Capturamos el contenido de rating--wrap--b76FfDS
rating_element = browser.find_element_by_class_name("rating--wrap--b76FfDS")
strong_element = rating_element.find_element_by_tag_name("strong")
valoracion_01 = strong_element.text

# Capturamos el contenido de a2g0o.detail.0.0
review_element = browser.find_element_by_css_selector("a[href*='a2g0o.detail.0.0']")
cant_review_01 = review_element.text.split(" ")[0]  # Tomamos solo el número (706)

# Capturamos el contenido de ventas
ventas_element = browser.find_element_by_css_selector("span:nth-child(3)")
cant_vendidos_01 = ventas_element.text.split("+")[0]  # Tomamos solo el número (3.000)

# Cerrar el navegador
browser.quit()

# Imprimimos las variables para verificar
print("Valoración:", valoracion_01)
print("Cantidad de Reviews:", cant_review_01)
print("Cantidad Vendidos:", cant_vendidos_01)