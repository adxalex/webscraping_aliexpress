import time
from whatsapp import whatsapp
from bd_productos import bd_productos
from proveedores import seleccionar_proveedor
from operaciones import obtener_precio_stock, compara_precio_stock
from selenium.common.exceptions import NoSuchElementException

import time

def main():
    while True:
        productos = bd_productos()
        for producto in productos:
            try:
                url = producto['url']
                precio_proveedor = producto['precio_proveedor']
                nombre_producto = producto['nombre_prd']

                proveedor = seleccionar_proveedor(url)
                precio_en_linea = obtener_precio_stock(url, proveedor)

                resultado_comparacion, precio_proveedor, precio_en_linea = compara_precio_stock(precio_proveedor, precio_en_linea)


                if resultado_comparacion:
                    print("Mensaje: Se mantiene el precio")
                else:
                    mensaje_comparacion = f'El articulo {nombre_producto} Ha cambiado el precio de {precio_proveedor} a {precio_en_linea}'
                    print(mensaje_comparacion)
                    # whatsapp(mensaje_comparacion)

            except NoSuchElementException as e:
                print(f"No se encontró el elemento: {e}")
            except Exception as e:
                print(f"Ocurrió un error al obtener la información: {e}")

        print("Esperando una hora antes de la siguiente verificación...")
        time.sleep(3600)


# Ejecutar el script principal
if __name__ == "__main__":
    main()
