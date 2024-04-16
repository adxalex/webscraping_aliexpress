from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pickle



def guardar_inicio_sesion(url, proveedor):
    # Inicia el navegador y autentícate manualmente en el sitio.
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(500)  # Espera un minuto para que puedas iniciar sesión manualmente.

    if proveedor == 'amazon':
        # Guarda las cookies después de haber iniciado sesión
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    elif proveedor == 'aliexpress':
        pickle.dump(driver.get_cookies(), open("cookies_aliexpress.pkl", "wb"))

    # Puedes cerrar el navegador después de guardar las cookies
    driver.quit()

url = 'https://ds.aliexpress.com/#/hot-search?title=Winning%20Products'
proveedor = 'aliexpress'
guardar_inicio_sesion(url,proveedor)

def iniciar_selenium(url, proveedor):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)

        if proveedor == 'amazon':
            # Carga las cookies
            try:
                if proveedor == 'amazon':
                    cookies = pickle.load(open("cookies.pkl", "rb"))
                elif proveedor == 'aliexpress':
                    cookies = pickle.load(open("cookies_aliexpress.pkl", "rb"))

                for cookie in cookies:
                    driver.add_cookie(cookie)
            except FileNotFoundError:
                print("Archivo de cookies no encontrado.")
            except Exception as e:
                print(f"Error al cargar cookies: {e}")

        # Accede al sitio como un usuario autenticado
        driver.get(url)
        # Aquí iría el resto de tu código para extraer precios y guardarlos en la base de datos.

        return driver
    except Exception as e:
        print(f"Error al iniciar Selenium: {e}")
        return None

# Usar la función
#driver = iniciar_selenium('https://www.aliexpress.com', 'aliexpress')


#url = 'https://es.aliexpress.com/item/1005005861980798.html?spm=a2g0o.productlist.main.1.b6aaw2jxw2jx59&algo_pvid=46bc516a-c674-4563-8951-1b868e39e272&aem_p4p_detail=202401311353443674780110941590001458739&algo_exp_id=46bc516a-c674-4563-8951-1b868e39e272-0&pdp_npi=4%40dis%21CLP%2127883%219592%21%21%21208.65%2171.78%21%402103242517067380241546343ef5ed%2112000034612635010%21sea%21CL%214379417073%21&curPageLogUid=w1ajtcxhjFwb&utparam-url=scene%3Asearch%7Cquery_from%3A&search_p4p_id=202401311353443674780110941590001458739_1'
#proveedor = 'amazon'
#proveedor = 'aliexpress'
#guardar_inicio_sesion(url, proveedor)