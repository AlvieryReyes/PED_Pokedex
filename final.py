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
        df = TablaRegion.dropna().drop_duplicates()
        for _, row in df.iterrows():
            sql = """INSERT IGNORE INTO region (Nombre) VALUES (%s)"""
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
        df = TablaPokedex.dropna().drop_duplicates()
        for _, row in df.iterrows():
            sql = """INSERT IGNORE INTO pokedex (Numero_de_pokedex, Nombre_de_pokemon, Region_id) VALUES (%s, %s, %s)"""
            data = (row['Numero de Pokedex'], row['Nombre de Pokemon'], row['Region_id'])
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
        df = TablaTipos.dropna().drop_duplicates()
        for _, row in df.iterrows():
            sql = """INSERT IGNORE INTO tipos (Nombre) VALUES (%s)"""
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

def webscrapingPokedex(region_mapping):
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
            region_name = cols[2].text.strip() if len(cols) > 2 else None
            region_id = region_mapping.get(region_name, None)
            if pokedex_numero.isdigit():
                pokedex_data.append({'Numero de Pokedex': pokedex_numero, 'Nombre de Pokemon': nombre, 'Region_id': region_id})

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

def dibujar(data_combined: pd.DataFrame):
    # Gráfico de barras apiladas: Pokémon por región y tipo
    fig_regiones_tipos = px.bar(
        data_combined,
        x='region_name',
        color='tipo_name',
        title='Distribución de Pokémon por Región y Tipo',
        labels={'region_name': 'Región', 'tipo_name': 'Tipo'}
    )

    # Mapa de calor (heatmap) de tipos por región
    heatmap_data = data_combined.groupby(['region_name', 'tipo_name']).size().reset_index(name='count')
    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x='region_name',
        y='tipo_name',
        z='count',
        title='Mapa de Calor de Tipos por Región',
        labels={'region_name': 'Región', 'tipo_name': 'Tipo', 'count': 'Cantidad'}
    )

    body = html.Div([
        html.H1("Dashboard de Pokémon", style={"textAlign": "center", "color": "#FFCC00"}),

        html.Div([
            html.H2("Distribución de Pokémon por Región y Tipo"),
            dcc.Graph(figure=fig_regiones_tipos)
        ], style={"padding": "10px", "backgroundColor": "#1E1E1E", "color": "white"}),

        html.Div([
            html.H2("Mapa de Calor de Tipos por Región"),
            dcc.Graph(figure=fig_heatmap)
        ], style={"padding": "10px", "backgroundColor": "#1E1E1E", "color": "white"}),
    ])

    return body

if __name__ == "__main__":
    print("Iniciando scraping y configuración de datos...")
    df_regiones = webscrapingRegion()
    region_mapping = {row['Nombre']: idx + 1 for idx, row in df_regiones.iterrows()}

    df_pokedex = webscrapingPokedex(region_mapping)
    df_tipos = webscrappingTipos()

    conexion_db = conexion()
    if conexion_db:
        importarDatosRegion(conexion_db, df_regiones)
        importarDatosPokedex(conexion_db, df_pokedex)
        importarDatosTipos(conexion_db, df_tipos)
        conexion_db.close()

        engine = create_engine('mysql+mysqlconnector://root:psp20020@localhost:3306/Pokemon')
        query = """
        SELECT p.Nombre_de_pokemon, r.Nombre AS region_name, t.Nombre AS tipo_name
        FROM pokedex p
        LEFT JOIN region r ON p.Region_id = r.id
        LEFT JOIN tipos t ON t.id IN (SELECT tipo_id FROM pokemon_tipos WHERE pokemon_id = p.id)
        """
        data_combined = pd.read_sql(query, engine)

        app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
        app.layout = dibujar(data_combined)
        app.run(debug=True)
    else:
        print("No se pudo conectar a la base de datos.")
