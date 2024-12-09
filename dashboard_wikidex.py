import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table

def graph(data_pokedex: pd.DataFrame, data_tipos: pd.DataFrame, data_regiones: pd.DataFrame):
    fig_pokedex = px.scatter(
        data_pokedex,
        x='Numero_de_pokedex',
        y='Nombre_de_pokemon',
        title='Distribución de Pokemon'
    )
    fig_tipos_pie = px.pie(data_tipos, names='Nombre', title='Distribución de Tipos de Pokemon')
    fig_regiones_bar = px.bar(data_regiones, x='Nombre', title='Cantidad de Pokemon por Region')

    body = html.Div([
        html.H1("Dashboard de Pokemon", style={"textAlign": "center"}),
        dcc.Graph(figure=fig_pokedex),
        dcc.Graph(figure=fig_tipos_pie),
        dcc.Graph(figure=fig_regiones_bar)
    ])
    return body
