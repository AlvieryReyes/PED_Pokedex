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
            print('Good: Conexion exitosa.')
            return conexion
    except Error as ex:
        print('Error: Conexion fallida.', ex)
        return None

def import_region(conexion, TablaRegion):
    try:
        cursor = conexion.cursor()
        df = TablaRegion.dropna()
        for _, row in df.iterrows():
            sql = """INSERT INTO region (Nombre) VALUES (%s)"""
            data = (row['Nombre'],)
            cursor.execute(sql, data)
        conexion.commit()
        print('Good: Datos de la tabla region insertados.')
    except Error as ex:
        print('Error: Datos en region no insertados:', ex)
    finally:
        cursor.close()

def import_pokedex(conexion, TablaPokedex):
    try:
        cursor = conexion.cursor()
        df = TablaPokedex.dropna()
        for _, row in df.iterrows():
            sql = """INSERT INTO pokedex (Numero_de_pokedex, Nombre_de_pokemon) VALUES (%s, %s)"""
            data = (row['Numero de Pokedex'], row['Nombre de Pokemon'])
            cursor.execute(sql, data)
        conexion.commit()
        print('Good: Datos Pokedex insertados.')
    except Error as ex:
        print('Error: Datos en la Pokedex no insertados:', ex)
    finally:
        cursor.close()

def import_tipos(conexion, TablaTipos):
    try:
        cursor = conexion.cursor()
        df = TablaTipos.dropna()
        for _, row in df.iterrows():
            sql = """INSERT INTO tipos (Nombre) VALUES (%s)"""
            data = (row['Nombre'],)
            cursor.execute(sql, data)
        conexion.commit()
        print('Good: Datos de la tabla tipos insertados.')
    except Error as ex:
        print('Error: Datos en la tabla tipos no insetados:', ex)
    finally:
        cursor.close()
