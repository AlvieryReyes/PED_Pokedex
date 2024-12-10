#Iniciamos importando la librería correspondiente a MySQL, la cual es mysql.connector, que nos ayudará a movernos
#dentro de este programa y hacer modificaciones e inserciones. 

import mysql.connector
from mysql.connector import Error


#en este caso se harán las inserciones de los 
#datos que recuperamos y guardamos en los dataframes.

#Específicamente las cosas que pasaremos serán los datos de la tabla (Dataframe) región de los poquemones 
#También de Pokedex y los tipos de pokemon existentes que recuperamos

#Generamos la conexión
def conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='password',  #favor de escribir su contraseña para que funcione :)
            database='Pokemon'
        )
        if conexion.is_connected():
            print('Good: Conexion exitosa.')
            return conexion
    except Error as ex:
        print('Error: Conexion fallida.', ex)
        return None

#Crearmos una función que herede la conexion e mysql de la funcion "Conexión", importamos la tabla region y 
#Generaremos las inserciones por medio de un for que tomará como referencia las rows del dataframe para 
#Hacer las inserciones en MySQL

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
    #Una vez se acabe, se cerrará la conexión a mysql
    finally:
        cursor.close()

#Generamos otra función ahora para exportar a la tabla de MySQL los datos del DataFrame "Pokedex" que ya teníamos en otro script de web scrping
#Y se hace lo mismo que en el anterior hasta la tabla de tipos 
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
#Se hace lo mismo que en las otras funciones pasadas
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
