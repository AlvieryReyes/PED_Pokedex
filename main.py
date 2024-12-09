import pandas as pd
from sqlalchemy import create_engine
from dash import Dash

from webscraping_wikidex import webscraping_region, webscraping_pokedex, webscraping_tipos
from conectividadDB_wikidex import conexion, importar_datos
from dashboard_wikidex import crear_dashboard

if __name__ == "__main__":
    print("Iniciando scraping de datos...")
    df_regiones = webscraping_region()
    df_pokedex = webscraping_pokedex()
    df_tipos = webscraping_tipos()

    print("\nConectando a la base de datos...")
    conexion_db = conexion()
    if conexion_db:
        importar_datos(conexion_db, 'region', df_regiones)
        importar_datos(conexion_db, 'pokedex', df_pokedex)
        importar_datos(conexion_db, 'tipos', df_tipos)
        conexion_db.close()
        print("\nDatos importados correctamente.")

        print("\nGenerando visualización...")
        # Configuración de la conexión para consulta
        engine = create_engine('mysql+mysqlconnector://root:psp20020@localhost:3306/Pokemon')
        data_pokedex = pd.read_sql("SELECT * FROM pokedex", engine)
        data_tipos = pd.read_sql("SELECT * FROM tipos", engine)
        data_regiones = pd.read_sql("SELECT * FROM region", engine)

        # Configuración de la aplicación Dash
        app = Dash(__name__)
        app.layout = crear_dashboard(data_pokedex, data_tipos, data_regiones)
        app.run(debug=True)
    else:
        print("Error: No se pudo conectar a la base de datos.")
