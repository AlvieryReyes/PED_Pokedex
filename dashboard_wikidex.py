import plotly.express as px
from dash import Dash, html, dcc, dash_table

def dibujar(data_pokedex, data_tipos, data_regiones):
    fig_pokedex = px.scatter(
        data_pokedex,
        x='Numero_de_pokedex',
        y='Nombre_de_pokemon',
        title='Distribucion de Pokemon'
    )
    fig_tipos_pie = px.pie(
        data_tipos,
        names='Nombre',
        title='Distribucion de Tipos de Pokemon'
    )
    fig_regiones = px.bar(
        data_regiones,
        x='Nombre',
        title='Regiones de Pokemon'
    )
    return html.Div([
        dcc.Graph(figure=fig_pokedex),
        dcc.Graph(figure=fig_tipos_pie),
        dcc.Graph(figure=fig_regiones)
    ])
