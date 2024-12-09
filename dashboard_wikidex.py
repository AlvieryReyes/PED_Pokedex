import plotly.express as px
from dash import Dash, html, dcc, dash_table

def crear_dashboard(data_pokedex, data_tipos, data_regiones):
    # Gráfica de cantidad de Pokémon por tipo
    fig_tipos_bar = px.bar(
        data_tipos,
        x='Nombre',
        title='Cantidad de Pokémon por Tipo',
        template='plotly_dark'
    )
    fig_tipos_bar.update_layout(
        xaxis_title="Tipo",
        yaxis_title="Cantidad",
        paper_bgcolor='black'
    )

    # Gráfica de Pokémon por región
    fig_regiones = px.bar(
        data_regiones,
        x='Nombre',
        title='Cantidad de Pokémon por Región',
        template='plotly_dark'
    )
    fig_regiones.update_layout(
        xaxis_title="Región",
        yaxis_title="Cantidad",
        paper_bgcolor='black'
    )

    # Gráfica de dispersión de Pokémon en la Pokédex
    fig_pokedex = px.scatter(
        data_pokedex,
        x='Numero_de_pokedex',
        y='Nombre_de_pokemon',
        title='Distribución de Pokémon en la Pokédex',
        template='plotly_dark'
    )
    fig_pokedex.update_layout(
        xaxis_title="Número de Pokédex",
        yaxis_title="Nombre de Pokémon",
        paper_bgcolor='black'
    )

    # Tabla interactiva con datos
    tabla_pokedex = dash_table.DataTable(
        data=data_pokedex.to_dict("records"),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_header={'backgroundColor': 'black', 'color': 'white'},
        style_cell={'backgroundColor': 'black', 'color': 'white'}
    )

    # Diseño general del dashboard
    app_layout = html.Div([
        html.H1("Dashboard de Pokémon", style={"textAlign": "center", "color": "yellow"}),
        dcc.Graph(figure=fig_tipos_bar),
        dcc.Graph(figure=fig_regiones),
        dcc.Graph(figure=fig_pokedex),
        html.H3("Tabla de Datos de la Pokédex", style={"color": "white"}),
        tabla_pokedex
    ], style={"backgroundColor": "#1E1E1E", "padding": "20px"})

    return app_layout
