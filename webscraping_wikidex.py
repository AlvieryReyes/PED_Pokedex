#Lo primero que tendremos que hacer serán las importaciones de varias librerías, las cuales esteremos usando para movernos dentro de
#el navegador Chrome, después poder guardar los datos dentro de un dataframe donde usaremos pandas.

#Selenium nos ayudará en bastantes cosas, como hacer un cursor, que es el que "dará" click en el lugar correspondiente.
#By de selenium nos ayudará a darle instrucciones al cursor de qué cosas buscar, ya sea ID, clase, nombre, etc. De las etiquetas
#Service nos ayudará en la gestión de ejecución en el navegador
#Driver nos ayuda también en gestiones movimientos
#time para que el cursor espere entre acciones, de tal manera que no se detecte como robot

#Beautiful soup será muy utilizada también y es fundamental para analizar documentos y códigos HTML y poder extraer
#esos datos

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

#una vez importadas todas las librerías que usaremos iniciamos con el código

#Creamos una función para sacar las regiones de los pokemon donde agarramos la ruta, usando service y options para ver la ventana
#y el navegador entrará a la pagina

def ws_region():
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    options = Options()
    options.add_argument('--window-size=1020,1200')
    navegador = webdriver.Chrome(service=service, options=options)

    #Una vez que el navegador este dentro tendrá que encontrar el elemento "search" y escribirá región
    
    navegador.get('https://www.wikidex.net/wiki/WikiDex')
    txtBuscador = navegador.find_element(By.NAME, 'search')
    btnIr = navegador.find_element(By.NAME, 'go')
    txtBuscador.send_keys('region')

    #Una vez que lo encuentre y agregue region, hará click en "go" para que el buscador de la pagina de pokemons arroge resultados
    
    try:
        #Aqui le decimos al navegador que espere 10 segundos hasta que el elemento "go" se pueda hacer click
        WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.NAME, 'go')))
        btnIr.click()
    except ElementClickInterceptedException:
        navegador.execute_script("arguments[0].click();", btnIr)

    #Una vez hehco esperará 3 segundos y tendrá que encontrar las etiquetas "class":"toclevel-2"
    #Por medio de un ciclo se guardarán los datos en la variable regiones
    time.sleep(3)
    soup = BeautifulSoup(navegador.page_source, 'html.parser')
    items = soup.find_all('li', {'class': 'toclevel-2'})
    regiones = [{'Nombre': item.find('span', {'class': 'toctext'}).text.strip()} for item in items]

    #Posteriormente el navegador se cerrará
    navegador.quit()

    #Se crea un dataframe con los datos y también se pasaran a formato csv.
    df = pd.DataFrame(regiones)
    df.to_csv('region.csv', index=False)
    return df


#Se genera una nueva función para hacer lo mismo que en la anterior, pero esta funcionará para hacer un web scraping de pokedex
def ws_pokedex():

    #Se vuelve a generar la ruta y a establecer el tamaño de la ventana emergente
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    options = Options()
    options.add_argument('--window-size=1020,1200')
    navegador = webdriver.Chrome(service=service, options=options)

    #Aquí se le da al navegador el link de la página donde está la información que requerimos
    navegador.get('https://www.wikidex.net/wiki/Lista_de_Pok%C3%A9mon')
    time.sleep(5)
    
    #Una vez aquí le decimos qué es lo que queremos que encuentre, que en este caso son todas las "tr" etiquetas
    soup = BeautifulSoup(navegador.page_source, 'html.parser')
    rows = soup.find_all('tr')

    #Creamos una lista donde se irá guardando los datos, que será donde se agregue el diccionario
    pokedex_data = []

    #Generamos un ciclo for, del 1 al 355, ya que esa es la cantidad de datos que se extrageron, de tal forma que
    #el data frame coincida en cantidad de renglones con el otro
    for row in rows[1:355]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            pokedex_numero = cols[0].text.strip()
            nombre = cols[1].a.text.strip()
            if pokedex_numero.isdigit():
                pokedex_data.append({'Numero de Pokedex': pokedex_numero, 'Nombre de Pokemon': nombre})

    #El navegador se cierra y se pasa a DataFrame el diccionario anterior, así como de guardar los datos en un archivo csv
    navegador.quit()
    df = pd.DataFrame(pokedex_data)
    df.to_csv('Pokedex.csv', index=False)
    return df

#Volvemos a hacer el proceso pero ahora para estraer los tipos de pokemon que hay
def ws_Tipos():
    
    #Generamos el driver path que será nuestra conexión y delimintamos el atamaño de la pantalla que queremos usar 
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    options = Options()
    options.add_argument('--window-size=1020,1200')
    navegador = webdriver.Chrome(service=service, options=options)

    #Le damos al navegador la pagina que ocupa entrar 
    navegador.get('https://www.wikidex.net/wiki/Tipo')
    time.sleep(7)

    #Y a beautiful soup las etiquetas que tiene que extraer, que en este caso serían "class":"tabpokemon"
    soup = BeautifulSoup(navegador.page_source, 'html.parser')
    table = soup.find('table', {'class': 'tabpokemon'})

    #Por medio de un ciclo guardaremos el tipo de pokemon correspondiente con lo demás
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
