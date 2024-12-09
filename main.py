from webscraping import webscrapingRegion, webscrapingPokedex, webscrapingTipos
from database import conexion, importarDatosRegion, importarDatosPokedex, importarDatosTipos
from dashboard import dibujar
from dash import Dash
import pandas as pd
from sqlalchemy import create_engine

# Web scraping
df_regiones = webscrapingRegion()
df_pokedex = webscrapingPokedex()
df_tipos = webscrapingTipos()

# Base de datos
conexion_db = conexion()
if conexion_db:
    importarDatosRegion(conexion_db, df_regiones)
    importarDatosPokedex(conexion_db, df_pokedex)
    importarDatosTipos(conexion_db, df_tipos)
    conexion_db.close()

# Dashboards
engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/Pokemon')
data_pokedex = pd.read_sql("SELECT * FROM pokedex", engine)
data_tipos = pd.read_sql("SELECT * FROM tipos", engine)
data_regiones = pd.read_sql("SELECT * FROM region", engine)

app = Dash(__name__)
app.layout = dibujar(data_pokedex, data_tipos, data_regiones)
app.run(debug=True)
