import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table

def dibujar(data_pokedex: pd.DataFrame, data_tipos: pd.DataFrame, data_regiones: pd.DataFrame):
    fig_pokedex = px.scatter(
        data_pokedex,
        x='Numero_de_pokedex',
        y='Nombre_de_pokemon',
        title='Distribución de Pokémon'
    )
    fig_tipos_pie = px.pie(data_tipos, names='Nombre', title='Distribución de Tipos de Pokémon')
    fig_regiones_bar = px.bar(data_regiones, x='Nombre', title='Cantidad de Pokémon por Región')

    body = html.Div([
        html.H1("Dashboard de Pokémon", style={"textAlign": "center"}),
        dcc.Graph(figure=fig_pokedex),
        dcc.Graph(figure=fig_tipos_pie),
        dcc.Graph(figure=fig_regiones_bar)
    ])
    return body
