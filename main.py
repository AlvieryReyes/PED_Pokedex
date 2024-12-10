# Este es el script que ejecutará todo como debe de ir, aquí está el name==main, donde abajo se encuentran todas las funciones creadas en los otors scripts

#Importamos las funciones que se crearon en los otros scripts, empezando por el webscraping, donde estan los dataframes de region, pokedex, y los tipos de pokemon
from webscraping_wikidex import ws_region, ws_pokedex, ws_Tipos

#Se importan las conectividades a MySQL, así como la exportación de los Dataframes 
from conectividadDB_wikidex import conexion, import_region, import_pokedex, import_tipos

#Se generan los dashboards que se hicieron enel script dashboard_wikidex
from dashboard_wikidex import graph

#Motor de python a MySQL
from sqlalchemy import create_engine

#Estas son las librerias que ya hemos usado en los otros scripts
import pandas as pd
from dash import Dash
import dash_bootstrap_components as dbc

#Se empiezan a ejecutar los códigos iniciando con el web scraper donde se almacenarion la region, pokedex y los tipos transformados a dataframes,
#Una vez hehco eso los guardamos en variables iniciando con df_ para saber que son ata Frames
if __name__ == "__main__":
    print("Iniciando scraping y configuración de datos...")
    df_regiones = ws_region()
    df_pokedex = ws_pokedex()
    df_tipos = ws_Tipos()

    #Empezamos con la conexión a MySQL y la exportación de los dataframes
    conexion_db = conexion()
    if conexion_db:
        import_region(conexion_db, df_regiones)
        import_pokedex(conexion_db, df_pokedex)
        import_tipos(conexion_db, df_tipos)
        conexion_db.close()

        #Aquí nos conectamos a la base de datos y podemos leer y ver las inserciones que se realizaron previamente
        engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/Pokemon') #favor de escribir su contraseña para que funcione :)
        data_pokedex = pd.read_sql("SELECT * FROM pokedex", engine)
        data_tipos = pd.read_sql("SELECT * FROM tipos", engine)
        data_regiones = pd.read_sql("SELECT * FROM region", engine)

        #una vez hehco esto se empiezan a generar y visualizar los dataframes de manera gráfica, tanto de pokedex, como los tipos de pokemon y las regiones
        app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
        app.layout = graph(data_pokedex, data_tipos, data_regiones)
        app.run(debug=True)
