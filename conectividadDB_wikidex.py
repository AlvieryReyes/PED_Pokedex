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
            print('Conexion exitosa a la base de datos.')
            return conexion
    except Error as ex:
        print('Error durante la conexion:', ex)
        return None

def importarDatosRegion(conexion, TablaRegion):
    try:
        cursor = conexion.cursor()
        for _, row in TablaRegion.iterrows():
            sql = "INSERT INTO region (Nombre) VALUES (%s)"
            cursor.execute(sql, (row['Nombre'],))
        conexion.commit()
        print('Datos de la tabla region insertados correctamente.')
    finally:
        cursor.close()

def importarDatosPokedex(conexion, TablaPokedex):
    try:
        cursor = conexion.cursor()
        for _, row in TablaPokedex.iterrows():
            sql = "INSERT INTO pokedex (Numero_de_pokedex, Nombre_de_pokemon) VALUES (%s, %s)"
            cursor.execute(sql, (row['Numero de Pokedex'], row['Nombre de Pokemon']))
        conexion.commit()
        print('Datos de la Pokedex insertados correctamente.')
    finally:
        cursor.close()

def importarDatosTipos(conexion, TablaTipos):
    try:
        cursor = conexion.cursor()
        for _, row in TablaTipos.iterrows():
            sql = "INSERT INTO tipos (Nombre) VALUES (%s)"
            cursor.execute(sql, (row['Nombre'],))
        conexion.commit()
        print('Datos de la tabla tipos insertados correctamente.')
    finally:
        cursor.close()
