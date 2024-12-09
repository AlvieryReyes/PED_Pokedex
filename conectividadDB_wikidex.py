import mysql.connector
from mysql.connector import Error

def conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='psp20020',
            database='Pokemon'
        )
        if conexion.is_connected():
            print('Conexión exitosa a la base de datos.')
            return conexion
    except Error as ex:
        print('Error durante la conexión:', ex)
        return None

def importar_datos(conexion, tabla, datos):
    try:
        cursor = conexion.cursor()
        df = datos.dropna()  # Eliminar valores nulos para evitar errores
        if tabla == 'region':
            sql = "INSERT INTO region (Nombre) VALUES (%s)"
            data_to_insert = [(row['Nombre'],) for _, row in df.iterrows()]
        elif tabla == 'pokedex':
            sql = "INSERT INTO pokedex (Numero_de_pokedex, Nombre_de_pokemon) VALUES (%s, %s)"
            data_to_insert = [(row['Numero de Pokedex'], row['Nombre de Pokemon']) for _, row in df.iterrows()]
        elif tabla == 'tipos':
            sql = "INSERT INTO tipos (Nombre) VALUES (%s)"
            data_to_insert = [(row['Nombre'],) for _, row in df.iterrows()]
        else:
            raise ValueError("Tabla no soportada.")

        cursor.executemany(sql, data_to_insert)
        conexion.commit()
        print(f'Datos de la tabla {tabla} insertados correctamente.')
    except Error as ex:
        print(f'Error al insertar datos en {tabla}:', ex)
    finally:
        cursor.close()
