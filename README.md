# Proyecto de Web Scraping y Visualización de Datos de WikiDex

Este proyecto consiste en un conjunto de scripts en Python que realizan web scraping en la página de WikiDex para obtener información sobre Pokémon y sus características. Los datos recopilados se almacenan en una base de datos MySQL y se visualizan en un dashboard interactivo con Dash y Plotly.


## Contenido
- [Descripcion del proyecto](#descripcion)
- [Requisitos](#requisitos)
- [Estructura del proyecto]()
- [Scripts](https://github.com/AlvieryReyes/PED_Pokedex/edit/main/scripts/README.md)
- [Notas](https://github.com/AlvieryReyes/PED_Pokedex/edit/main/notas/README.md)

## Descripcion
Este proyecto está compuesto por cuatro scripts principales que cumplen con las siguientes funciones:

1. Web Scraping de WikiDex: Extrae datos de la página web de WikiDex sobre regiones, Pokémon y tipos de Pokémon.
2. Conexión y Exportación a la Base de Datos: Inserta los datos extraídos en una base de datos MySQL.
3. Carga de Datos y Visualización: Crea un dashboard interactivo con Dash y Plotly para representar los datos de manera gráfica.
4. Script Principal: Orquesta la ejecución de los procesos de web scraping, conexión a la base de datos y visualización de los datos.

## Requisitos
Para ejecutar este proyecto, necesitas tener instaladas las siguientes bibliotecas de Python:

- `selenium`: Para la automatización de la navegación web
- `beautifulsoup4`: Para la extracción de datos de las páginas web.
- `pandas`: Para la manipulación y análisis de datos.
- `mysql-connector-python`: Para la conexión con la base de datos MySQL.
- `plotly`: Para la creación de gráficos interactivos.
- `dash`: Para la construcción de aplicaciones web interactivas.
- `dash-bootstrap-components`: Para aplicar estilos y temas a las aplicaciones Dash.
- `sqlalchemy`: Para la interacción con la base de datos mediante SQL.
- `webdriver-manager`: Para gestionar automáticamente el controlador de Chrome.

### Instalacion
```
pip install selenium beautifulsoup4 pandas mysql-connector-python plotly dash dash-bootstrap-components sqlalchemy webdriver-manager

```
