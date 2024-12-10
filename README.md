# Proyecto de Web Scraping y Visualización de Datos de WikiDex

Este proyecto consiste en un conjunto de scripts en Python que realizan web scraping en la página de WikiDex para obtener información sobre Pokémon y sus características. Los datos recopilados se almacenan en una base de datos MySQL y se visualizan en un dashboard interactivo con Dash y Plotly.


## Contenido
- [Descripcion del proyecto](#descripcion)
- [Requisitos](#requisitos)
- [Estructura del proyecto](#estructura)
- [Scripts](scripts)
- [Notas](notas)

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
## Estructura
El proyecto está compuesto por los siguientes archivos:

 1. webscraping_wikidex.py: Script que realiza el web scraping de la página de WikiDex y extrae información sobre regiones, Pokémon y tipos de Pokémon.
 2. conectividadDB_wikidex.py: Script que se conecta a la base de datos MySQL y exporta los datos a las tablas correspondientes.
 3. dashboard_wikidex.py: Contiene la función para crear el dashboard interactivo con gráficos usando Dash y Plotly.
 4. main.py: Script principal que orquesta la ejecución de los procesos de web scraping, inserción de datos y visualización

## Scripts
### Web Scraping de WikiDex (webscraping_wikidex.py)
Este script contiene las siguientes funciones:

- `ws_region()`:

Navega a la página de WikiDex y busca las regiones de Pokémon.
Extrae los nombres de las regiones y los guarda en un archivo CSV llamado region.csv.

- `ws_pokedex()`:

Accede a la lista de Pokémon en WikiDex y extrae los números de la Pokédex y los nombres de los Pokémon.
Guarda estos datos en un archivo CSV llamado Pokedex.csv.

- `ws_Tipos()`:

Extrae los tipos de Pokémon de la página de WikiDex y los guarda en un archivo CSV llamado tipos.csv.

### Conexión y Exportación a la Base de Datos (conectividadDB_wikidex.py)
Este script permite la conexión a una base de datos MySQL y la importación de datos a las tablas `region`, `pokedex` y `tipos`.

- `conexion()`:

Establece una conexión con la base de datos MySQL y devuelve el objeto de conexión.
- `import_region()`, `import_pokedex()`, `import_tipos()`:

 Inserta los datos de los DataFrame en las tablas correspondientes de la base de datos.
 
### Dashboard Interactivo (dashboard_wikidex.py)
Este script contiene la función `graph()`, que utiliza Dash y Plotly para crear un dashboard interactivo con los siguientes gráficos:

- Gráfico de dispersión que muestra la distribución de los Pokémon por número en la Pokédex.
- Gráfico circular (pie chart) para visualizar la distribución de los tipos de Pokémon.
- Gráfico de barras que presenta la cantidad de Pokémon por región.

### Script Principal (main.py)
El script `main.py` aplica la ejecución de los procesos del proyecto:

1. Llama a las funciones de web scraping y guarda los datos en DataFrame.
2. Se conecta a la base de datos MySQL y exporta los datos.
3. Crea un motor de conexión y carga los datos desde la base de datos.
4. Ejecuta la aplicación Dash para mostrar el dashboard interactivo.

## Notas
- Base de datos: Asegúrate de tener MySQL corriendo y la base de datos `Pokemon` creada antes de ejecutar el proyecto.
- Credenciales: Modifica las credenciales de la base de datos en el código (`root`, `password`, `localhost`) según tu configuración.
- Dependencias: La versión del controlador de Chrome debe ser compatible con tu versión de Chrome. Usa `webdriver-manager` para manejar esto automáticamente.
