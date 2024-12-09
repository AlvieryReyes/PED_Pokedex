from webscraping_wikidex import ws_region, ws_pokedex, ws_Tipos
from conectividadDB_wikidex import conexion, import_region, import_pokedex, import_tipos
from dashboard_wikidex import graph
from sqlalchemy import create_engine
import pandas as pd
from dash import Dash
import dash_bootstrap_components as dbc

if __name__ == "__main__":
    print("Iniciando scraping y configuración de datos...")
    df_regiones = ws_region()
    df_pokedex = ws_pokedex()
    df_tipos = ws_Tipos()

    conexion_db = conexion()
    if conexion_db:
        import_region(conexion_db, df_regiones)
        import_pokedex(conexion_db, df_pokedex)
        import_tipos(conexion_db, df_tipos)
        conexion_db.close()

        engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/Pokemon')
        data_pokedex = pd.read_sql("SELECT * FROM pokedex", engine)
        data_tipos = pd.read_sql("SELECT * FROM tipos", engine)
        data_regiones = pd.read_sql("SELECT * FROM region", engine)

        app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
        app.layout = graph(data_pokedex, data_tipos, data_regiones)
        app.run(debug=True)
