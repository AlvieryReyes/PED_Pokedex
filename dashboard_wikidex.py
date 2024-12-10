#En este script lo que planea es generar los dashboards de los datos y la información recabada en el web scraping

#Usaremos pandas, ploty nos ayudará a hacer mejores gráficas.
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table

#Empezamos a generar la función

#Aquí que pasan todos los data frames y se empiezan a organizar y acomodar, con las etiquetas que 
#tendrán de forma horizontal y vertical de las gráficas

def graph(data_pokedex: pd.DataFrame, data_tipos: pd.DataFrame, data_regiones: pd.DataFrame):
    fig_pokedex = px.scatter(
        data_pokedex,
        x='Numero_de_pokedex', #Etiqueda horizontal
        y='Nombre_de_pokemon', #Etiqueta vertical
        title='Distribución de Pokemon' #Título de la tabla
    )
    fig_tipos_pie = px.pie(data_tipos, names='Nombre', title='Distribución de Tipos de Pokemon') #Se muestra el total de cada Pokemon 
    fig_regiones_bar = px.bar(data_regiones, x='Nombre', title='Cantidad de Pokemon por Region') #Cantidad total de pokemon por region

    #Esto nos ayuda a visualizarlo graficamente de distintas maneras
    body = html.Div([
        html.H1("Dashboard de Pokemon", style={"textAlign": "center"}),
        dcc.Graph(figure=fig_pokedex), #Lo grafica en figura plotly
        dcc.Graph(figure=fig_tipos_pie), #Lo grafica en modo de pastel
        dcc.Graph(figure=fig_regiones_bar) #Se grafica en barras
    ])
    return body
