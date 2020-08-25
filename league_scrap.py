from bs4 import BeautifulSoup   # Not built-in -- install with '!pip install beautifulsoup4'
import pandas as pd             # Not built-in -- install with '!pip install pandas'
import requests
from os import remove
from os import path

# Función que permite extraer las URL de los equipos pertenecientes a las LIGAS del sitio transfermartk.es
def page_scrap(x):
    headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = x
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')
    
    # Definir sección pivote para realizar scrap.
    pageClub = pageSoup.find_all('td', {"class":"hauptlink no-border-links hide-for-small hide-for-pad"})

    # Definir arrays para almacenar datos de Ligas (Club, ID  y URL)
    clubName = []
    clubURL = []
    clubID = []

    # Recorrer la sección definida como pivote.
    for i in pageClub:
        # Extraer el texto de la linea analizada
        clubName.append(i.text)

        # Avanzar a los 'a class' HTML para extraer la url del club
        web = i.find('a')
        clubURL.append(web.get('href')[:-4])
        
        clubID.append(web.get('id'))

    # Crear data frame con club y url para hacer scrap a jugadores
    df = pd.DataFrame({"League":pageSoup.title.string[:-22], 
                       "Club Name":clubName, 
                       "Club ID":clubID,
                       "Club URL":clubURL})
    
    return df.reset_index(drop=True)

# Declarar variables
dataLeague = pd.DataFrame()

# Leer <<archivo.csv>> que contiene el enlace de cada LIGA a Scrapear y lo transforma en DataFrame 
link = pd.read_csv("D:/my-projects/football-scrap/files/input_league_links.csv", sep=";") # Reemplazar por "league_links.csv"
dfLink = pd.DataFrame(link)

# Ejecuta la función page_scrap() 'n' veces como LINK de ligas vengan en el archivo
for i in dfLink['link']:
    dataLeague_temp = page_scrap(i)
    # Apilar los DataFrames uno encima del otro Vertical Stack
    dataLeague = pd.concat([dataLeague, dataLeague_temp], axis=0)
    del dataLeague_temp
    
    print("Cargando ", i, "de ", len(dfLink))

if path.exists("D:/my-projects/football-scrap/files/output_clubLink.csv"):
    remove('D:/my-projects/football-scrap/files/output_clubLink.csv')
    
dataLeague.to_csv('D:/my-projects/football-scrap/files/output_clubLink.csv', encoding='utf-8', index=False)