import mysql.connector
from mysql.connector import Error

def conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='psp20020',  #favor de escribir su contraseña para que funcione :)
            database='Pokemon'
        )
        if conexion.is_connected():
            print('Conexion exitosa a la base de datos.')
            return conexion
    except Error as ex:
        print('Error durante la conexion:', ex)
        return None

def importarDatosRegion(conexion, TablaRegion):
    try:
        cursor = conexion.cursor()
        df = TablaRegion.dropna()
        for _, row in df.iterrows():
            sql = """INSERT INTO region (Nombre) VALUES (%s)"""
            data = (row['Nombre'],)
            cursor.execute(sql, data)
        conexion.commit()
        print('Datos de la tabla region insertados correctamente.')
    except Error as ex:
        print('Error al insertar datos en region:', ex)
    finally:
        cursor.close()

def importarDatosPokedex(conexion, TablaPokedex):
    try:
        cursor = conexion.cursor()
        df = TablaPokedex.dropna()
        for _, row in df.iterrows():
            sql = """INSERT INTO pokedex (Numero_de_pokedex, Nombre_de_pokemon) VALUES (%s, %s)"""
            data = (row['Numero de Pokedex'], row['Nombre de Pokemon'])
            cursor.execute(sql, data)
        conexion.commit()
        print('Datos de la Pokedex insertados correctamente.')
    except Error as ex:
        print('Error al insertar datos en la Pokedex:', ex)
    finally:
        cursor.close()

def importarDatosTipos(conexion, TablaTipos):
    try:
        cursor = conexion.cursor()
        df = TablaTipos.dropna()
        for _, row in df.iterrows():
            sql = """INSERT INTO tipos (Nombre) VALUES (%s)"""
            data = (row['Nombre'],)
            cursor.execute(sql, data)
        conexion.commit()
        print('Datos de la tabla tipos insertados correctamente.')
    except Error as ex:
        print('Error al insertar datos en la tabla tipos:', ex)
    finally:
        cursor.close()
