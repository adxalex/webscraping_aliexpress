import pandas as pd

def bd_productos():
    # Asegúrate de que el archivo 'bd_productos.xlsx' esté en la misma carpeta que tu script.
    # Si no, proporciona la ruta completa al archivo.
    archivo_excel = 'bd_productos.xlsx'

    try:
        # Cargar el archivo de Excel en un DataFrame
        df = pd.read_excel(archivo_excel, engine='openpyxl')

        # Extraer los valores de las columnas específicas
        id_url = df['id_url'].tolist()  # Convertir la columna id_url en una lista
        url = df['url_proveedor'].tolist()  # Convertir la columna url_proveedor en una lista
        precio_proveedor = df['precio_original'].tolist()  # Convertir la columna precio_proveedor en una lista
        stock_actual = df['stock'].tolist()  # Convertir la columna stock en una lista
        nombre_prd = df['nombre_prd'].tolist()  # Convertir la columna stock en una lista

        # Puedes manipular o retornar los datos como prefieras.
        # Por ejemplo, retornar una lista de diccionarios con los datos:
        productos = []
        for i in range(len(df)):
            productos.append({
                'id_url': id_url[i],
                'url': url[i],
                'precio_proveedor': precio_proveedor[i],
                'stock_actual': stock_actual[i],
                'nombre_prd': nombre_prd[i]
            })

        return productos

    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return []

# prueba = bd_productos()
# print(prueba)