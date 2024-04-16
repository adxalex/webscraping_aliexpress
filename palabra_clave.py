# nombre_producto = "reloj para viaje"

def buscar_palabras_clave(nombre_producto):
    palabras_clave = ['viaje', 'viajes', 'equipaje', 'maleta', 'mochila']
    for palabra in palabras_clave:
        if palabra in nombre_producto:
            return True
    return False

# resultado = buscar_palabras_clave(nombre_producto, palabras_clave)
# print(resultado)
