import mysql.connector
import pandas as pd
from selenium import webdriver
import time
from selenium.common.exceptions import WebDriverException
from config import db_config
from navegador import iniciar_selenium
from palabra_clave import buscar_palabras_clave

# Configuración inicial
#CHROMEDRIVER_PATH = 'D:/onedrive/EzLifetech/analisis_producto/chromedriver-win64/chromedriver.exe'
url = 'https://ds.aliexpress.com/#/hot-search?title=Winning%20Products'
#os.environ["PATH"] += os.pathsep + os.path.dirname(CHROMEDRIVER_PATH)

#chrome_options = Options()
#chrome_options.add_argument("--headless")

def obtener_datos(retry_count=0):
    try:
        proveedor = 'aliexpress'
        browser = iniciar_selenium(url, proveedor)
        time.sleep(5)
        product_links_js = browser.execute_script("return document.querySelectorAll('a.cardWrap--AU6evWbQ');")
        # Guardar los enlaces de los primeros 10 productos en la lista
        product_links = [link.get_attribute('href') for link in product_links_js[:60]]
        print(product_links)
        data_list = []

        for product_link in product_links:
            browser.get(product_link)
            time.sleep(10)

            # Capturamos el nombre del producto
            nombre_producto = browser.execute_script('''
                var nombreProductoElement = document.querySelector("h1[data-pl='product-title']");
                return nombreProductoElement ? nombreProductoElement.textContent.trim() : "Elemento no encontrado";
            ''')
            val_palabra_clave = buscar_palabras_clave(nombre_producto)

            if val_palabra_clave == False:
                print(f'palabra clave no encontrada en nombre producto')
                continue
            else:
                valoracion_01 = browser.execute_script('''
                    var ratingElement = document.querySelector(".reviewer--wrap--sPGWrNq strong");
                    return ratingElement ? ratingElement.textContent : "Elemento no encontrado";
                ''')

                cant_vendidos_01 = browser.execute_script('''
                    var ventasElement = document.querySelector(".reviewer--wrap--sPGWrNq > span:last-child");
                    return ventasElement ? ventasElement.textContent.split("+")[0].trim() : "Elemento no encontrado";
                ''')

                # Si el texto tiene la palabra 'Vendidos', se la quitamos
                if 'Vendidos' in cant_vendidos_01:
                    cant_vendidos_01 = cant_vendidos_01.replace('Vendidos', '').strip()

                # Si el texto está vacío, le asignamos un valor de 0
                if not cant_vendidos_01:
                    cant_vendidos_01 = '0'

                cant_vendidos_01 = int(cant_vendidos_01.replace('.', '').replace(',', ''))


                # Obtenemos el timestamp actual y lo convertimos al formato correcto
                time_dato = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

                data_list.append([product_link, valoracion_01, cant_vendidos_01, nombre_producto, time_dato])
                print(data_list)

        # Cerrar el navegador
        browser.quit()
        return data_list

    except WebDriverException:
        print("Error con el navegador. Reiniciando...")
        browser.quit()  # Cierra el navegador
        retry_count += 1
        if retry_count < 2:  # por ejemplo, limitar a 3 intentos
            iniciar_selenium(url, proveedor)
            return obtener_datos(retry_count)
        else:
            print("Número máximo de intentos alcanzado. No se pudo obtener los datos.")
            return None

    print("Datos obtenidos")

resultados = obtener_datos()
# Imprimir los resultados para verificación
print(resultados)

def guardar_datos(data_list):
    try:
        # Conectar a la base de datos
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Insertar datos en la base de datos
        insert_query = (
            "INSERT INTO prd_win"
            "(url_producto, ranking, cant_vendidos, nombre_producto, time_dato) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        cursor.executemany(insert_query, data_list)
        cnx.commit()

        # Cerrar la conexión
        cursor.close()
        cnx.close()
        print("Guardando datos en base de datos...")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Cerrar la conexión
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
        print("Conexión cerrada.")

    print("Datos guardados")


print("Ejecutando el script...")

# while True:
#     data_list = obtener_datos()  # Obtiene una lista de datos
#     guardar_datos(data_list)  # Guarda todos los datos en mysql
#
#     print("Datos guardados. Esperando para la siguiente iteración...")
#     time.sleep(10)  # Pausa de 10 segundos antes de la siguiente iteración