from proveedores import amazon,aliexpress

def obtener_precio_stock(url, proveedor):
    precio = None
    if proveedor == 'amazon':
        precio = amazon(url)
    elif proveedor == 'aliexpress':
        precio = aliexpress(url)
    else:
        raise ValueError("Proveedor no soportado")

    return precio  # Solo devolvemos el precio
def compara_precio_stock(precio_proveedor, precio_en_linea):
    # Verificar si el precio es un string y reemplazar comas por puntos
    if isinstance(precio_proveedor, str):
        precio_actual = precio_proveedor.replace(',', '.')
    else:
        precio_actual = precio_proveedor

    if isinstance(precio_en_linea, str):
        precio_nuevo = precio_en_linea.replace(',', '.')
    else:
        precio_nuevo = precio_en_linea

    # Convierte ambos precios a float para comparación numérica precisa
    precio_actual = float(precio_actual) if precio_actual else 0
    precio_nuevo = float(precio_nuevo) if precio_nuevo else 0

    # Compara los precios y retorna según las condiciones dadas
    diferencia = abs(precio_nuevo - precio_actual)

    # Si la diferencia es mayor a 2, retorna False
    if diferencia > 2:
        return False, precio_actual, precio_nuevo
    # Si la diferencia es menor o igual a 2, retorna True
    else:
        return True, precio_actual, precio_nuevo


# precio_proveedor = 4
# precio_en_linea = 4.8
#
# prueba_rest = precio_proveedor - precio_en_linea
# prueba = compara_precio_stock(precio_proveedor, precio_en_linea)
# print(prueba)
# print(prueba_rest)