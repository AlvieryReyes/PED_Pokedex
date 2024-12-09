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
            password='psp20020', #favor de escribir su contraseña para que funcione :)
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
        print('Good: Datos region insertados.')
    except Error as ex:
        print('Error: Datos de region no insertados:', ex)
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
        print('Good: Datos tipos insertados.')
    except Error as ex:
        print('Error: Datos de tipos no insertados:', ex)
    finally:
        cursor.close()

def ws_region():
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

def ws_pokedex():
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

def ws_tipos():
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

def graph(data_pokedex: pd.DataFrame, data_tipos: pd.DataFrame, data_regiones: pd.DataFrame):
    fig_pokedex = px.scatter(
        data_pokedex,
        x='Numero_de_pokedex',
        y='Nombre_de_pokemon',
        title='Distribución de Pokémon',
        labels={'Numero_de_pokedex': 'Número de Pokédex', 'Nombre_de_pokemon': 'Nombre del Pokémon'}
    )

    #grafica pastel
    fig_tipos_pie = px.pie(
        data_tipos,
        names='Nombre',
        title='Distribución de Tipos de Pokémon'
    )

    #grafica de barras para las regiones de pokemon
    fig_regiones_bar = px.bar(
        data_regiones,
        x='Nombre',
        title='Cantidad de Pokémon por Región',
        labels={'Nombre': 'Región', 'value': 'Cantidad'}
    )

    #grafica de barras, Si los datos de tipos estan relacionados con regiones, si nos podria salir la grafica pero no esta relacionado :(
    fig_tipos_bar = px.bar(
        data_tipos,
        x='Nombre',
        title='Cantidad de Pokémon por Tipo',
        labels={'Nombre': 'Tipo', 'value': 'Cantidad'}
    )

    body = html.Div([
        html.H1("Dashboard de Pokémon", style={"textAlign": "center", "color": "#FFCC00"}),

        html.Div([
            html.H2("Distribución de Pokémon"),
            dcc.Graph(figure=fig_pokedex)
        ], style={"padding": "10px", "backgroundColor": "#1E1E1E", "color": "white"}),

        html.Div([
            html.H2("Distribución de Tipos de Pokémon"),
            dcc.Graph(figure=fig_tipos_pie)
        ], style={"padding": "10px", "backgroundColor": "#1E1E1E", "color": "white"}),

        html.Div([
            html.H2("Cantidad de Pokémon por Región"),
            dcc.Graph(figure=fig_regiones_bar)
        ], style={"padding": "10px", "backgroundColor": "#1E1E1E", "color": "white"}),

        html.Div([
            html.H2("Cantidad de Pokémon por Tipo"),
            dcc.Graph(figure=fig_tipos_bar)
        ], style={"padding": "10px", "backgroundColor": "#1E1E1E", "color": "white"}),

        html.H3("Tabla Interactiva de la Pokedex"),
        dash_table.DataTable(
            data=data_pokedex.to_dict("records"),
            columns=[{"name": col, "id": col} for col in data_pokedex.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': '#1E1E1E', 'color': 'white'},
            style_data={'backgroundColor': '#3E3E3E', 'color': 'white'}
        ),

        html.H3("Tabla Interactiva de Tipos de Pokémon"),
        dash_table.DataTable(
            data=data_tipos.to_dict("records"),
            columns=[{"name": col, "id": col} for col in data_tipos.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': '#1E1E1E', 'color': 'white'},
            style_data={'backgroundColor': '#3E3E3E', 'color': 'white'}
        ),

        html.H3("Tabla Interactiva de Regiones"),
        dash_table.DataTable(
            data=data_regiones.to_dict("records"),
            columns=[{"name": col, "id": col} for col in data_regiones.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_header={'backgroundColor': '#1E1E1E', 'color': 'white'},
            style_data={'backgroundColor': '#3E3E3E', 'color': 'white'}
        )
    ])

    return body

if __name__ == "__main__":
    print("Extrayendo datos..................")
    df_regiones = ws_region()
    df_pokedex = ws_pokedex()
    df_tipos = ws_tipos()

    conexion_db = conexion()
    if conexion_db:
        import_region(conexion_db, df_regiones)
        import_pokedex(conexion_db, df_pokedex)
        import_tipos(conexion_db, df_tipos)
        conexion_db.close()

        engine = create_engine('mysql+mysqlconnector://root:psp20020@localhost:3306/Pokemon') #favor de escribir su contraseña para que funcione :)
        data_pokedex = pd.read_sql("SELECT * FROM pokedex", engine)
        data_tipos = pd.read_sql("SELECT * FROM tipos", engine)
        data_regiones = pd.read_sql("SELECT * FROM region", engine)

        app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
        app.layout = graph(data_pokedex, data_tipos, data_regiones)
        app.run(debug=True)
    else:
        print("Error: Conexion fallida.")