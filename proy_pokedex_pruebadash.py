import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import mysql.connector
from mysql.connector import Error
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table
from sqlalchemy import create_engine

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
        df = TablaRegion.dropna()  # Eliminar valores nulos para evitar errores
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

def webscrapingRegion():
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    options = Options()
    options.add_argument('--window-size=1020,1200')
    navegador = webdriver.Chrome(service=service, options=options)

    navegador.get('https://www.wikidex.net/wiki/WikiDex')

    txtBuscador = navegador.find_element(By.NAME, 'search')
    btnIr = navegador.find_element(By.NAME, 'go')
    txtBuscador.send_keys('region')

    try:
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.NAME, 'go')))
        btnIr.click()
    except ElementClickInterceptedException:
        navegador.execute_script("arguments[0].click();", btnIr)

    time.sleep(3)

    soup = BeautifulSoup(navegador.page_source, 'html.parser')
    items = soup.find_all('li', {'class': 'toclevel-2'})

    regiones = [{'Nombre': item.find('span', {'class': 'toctext'}).text.strip()} for item in items]

    navegador.quit()
    df = pd.DataFrame(regiones)
    df.to_csv('region.csv', index=False)
    return df

def webscrapingPokedex():
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    options = Options()
    options.add_argument('--window-size=1020,1200')
    navegador = webdriver.Chrome(service=service, options=options)

    navegador.get('https://www.wikidex.net/wiki/Lista_de_Pok%C3%A9mon')
    time.sleep(5)

    soup = BeautifulSoup(navegador.page_source, 'html.parser')
    rows = soup.find_all('tr')

    pokedex_data = []
    for row in rows[1:355]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            pokedex_numero = cols[0].text.strip()
            nombre = cols[1].a.text.strip()
            if pokedex_numero.isdigit():
                pokedex_data.append({'Numero de Pokedex': pokedex_numero, 'Nombre de Pokemon': nombre})

    navegador.quit()
    df = pd.DataFrame(pokedex_data)
    df.to_csv('Pokedex.csv', index=False)
    return df

def webscrappingTipos():
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    options = Options()
    options.add_argument('--window-size=1020,1200')
    navegador = webdriver.Chrome(service=service, options=options)

    navegador.get('https://www.wikidex.net/wiki/Tipo')
    time.sleep(7)

    soup = BeautifulSoup(navegador.page_source, 'html.parser')
    table = soup.find('table', {'class': 'tabpokemon'})

    tipos = set()
    if table:
        for row in table.find_all('tr'):
            for cell in row.find_all('td'):
                link = cell.find('a')
                if link and 'title' in link.attrs:
                    tipo_nombre = link.attrs['title'].replace("Tipo ", "").strip()
                    if tipo_nombre:
                        tipos.add(tipo_nombre)

    navegador.quit()
    tipos_list = [{'Nombre': tipo} for tipo in sorted(tipos)]
    df = pd.DataFrame(tipos_list)
    df.to_csv('tipos.csv', index=False)
    return df

def dibujar(data_pokedex: pd.DataFrame, data_tipos: pd.DataFrame, data_regiones: pd.DataFrame):
    # Grafica de dispersion para los datos de la Pokedex
    fig_pokedex = px.scatter(
        data_pokedex,
        x='Numero_de_pokedex',
        y='Nombre_de_pokemon',
        title='Distribucion de Pokemon'
    )
    fig_pokedex.update_layout(xaxis_title="Numero de Pokedex", yaxis_title="Nombre de Pokemon")

    # Grafica de pastel para los tipos de Pokemon
    fig_tipos_pie = px.pie(
        data_tipos,
        names='Nombre',
        title='Distribucion de Tipos de Pokemon'
    )

    # Grafica de barras para las regiones de Pokemon
    fig_regiones = px.bar(
        data_regiones,
        x='Nombre',
        title='Regiones de Pokemon'
    )
    fig_regiones.update_layout(xaxis_title="Region", yaxis_title="Cantidad")

    # Crear el diseno de la aplicacion con Dash
    body = html.Div([
        html.H2("Visualizacion de Datos de Pokemon", style={"textAlign": "center", "color": "yellow"}),
        html.P("Exploracion de datos de la Pokedex, tipos y regiones de Pokemon."),
        html.Hr(),
        dcc.Graph(figure=fig_pokedex),
        dcc.Graph(figure=fig_tipos_pie),
        dcc.Graph(figure=fig_regiones),
        html.H3("Tabla de la Pokedex"),
        dash_table.DataTable(
            data=data_pokedex.to_dict("records"),
            page_size=5,
            style_table={'overflowX': 'auto'}
        ),
        html.H3("Tabla de Tipos de Pokemon"),
        dash_table.DataTable(
            data=data_tipos.to_dict("records"),
            page_size=5,
            style_table={'overflowX': 'auto'}
        ),
        html.H3("Tabla de Regiones de Pokemon"),
        dash_table.DataTable(
            data=data_regiones.to_dict("records"),
            page_size=5,
            style_table={'overflowX': 'auto'}
        )
    ], style={"backgroundColor": "#1E1E1E", "color": "white", "padding": "20px"})

    return body

if __name__ == "__main__":
    print("Iniciando scraping de regiones...")
    df_regiones = webscrapingRegion()
    print(df_regiones.head())

    print("\nIniciando scraping de la Pokedex...")
    df_pokedex = webscrapingPokedex()
    print(df_pokedex.head())

    print("\nIniciando scraping de tipos...")
    df_tipos = webscrappingTipos()
    print(df_tipos.head())

    print("\nConectando a la base de datos...")
    conexion_db = conexion()
    if conexion_db:
        print("\nImportando datos a la base de datos...")
        importarDatosRegion(conexion_db, df_regiones)
        importarDatosPokedex(conexion_db, df_pokedex)
        importarDatosTipos(conexion_db, df_tipos)
        conexion_db.close()
        print("\nDatos importados correctamente.")

        print("\nConfigurando la aplicacion Dash...")
        engine = create_engine('mysql+mysqlconnector://root:psp20020@localhost:3306/Pokemon')

        # Consultas SQL para obtener datos
        query_pokedex = "SELECT * FROM pokedex"
        query_tipos = "SELECT * FROM tipos"
        query_region = "SELECT * FROM region"

        # Lectura de datos desde la base de datos
        data_pokedex = pd.read_sql(query_pokedex, engine)
        data_tipos = pd.read_sql(query_tipos, engine)
        data_regiones = pd.read_sql(query_region, engine)

        # Configuracion y ejecucion de la aplicacion Dash
        app = Dash(__name__)
        app.layout = dibujar(data_pokedex, data_tipos, data_regiones)
        app.run(debug=True)
    else:
        print("No se pudo conectar a la base de datos.")
