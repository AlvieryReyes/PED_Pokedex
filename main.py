from webscraping_wikidex import webscrapingRegion, webscrapingPokedex, webscrappingTipos
from conectividadDB_wikidex import conexion, importarDatosRegion, importarDatosPokedex, importarDatosTipos
from dashboard_wikidex import dibujar
from sqlalchemy import create_engine
import pandas as pd
from dash import Dash
import dash_bootstrap_components as dbc

if __name__ == "__main__":
    print("Iniciando scraping y configuración de datos...")
    df_regiones = webscrapingRegion()
    df_pokedex = webscrapingPokedex()
    df_tipos = webscrappingTipos()

    conexion_db = conexion()
    if conexion_db:
        importarDatosRegion(conexion_db, df_regiones)
        importarDatosPokedex(conexion_db, df_pokedex)
        importarDatosTipos(conexion_db, df_tipos)
        conexion_db.close()

        engine = create_engine('mysql+mysqlconnector://root:psp20020@localhost:3306/Pokemon')
        data_pokedex = pd.read_sql("SELECT * FROM pokedex", engine)
        data_tipos = pd.read_sql("SELECT * FROM tipos", engine)
        data_regiones = pd.read_sql("SELECT * FROM region", engine)

        app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
        app.layout = dibujar(data_pokedex, data_tipos, data_regiones)
        app.run(debug=True)
