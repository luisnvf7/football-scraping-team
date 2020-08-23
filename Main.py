import requests
from bs4 import BeautifulSoup
import pandas as pd

from datetime import datetime

headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

url = "https://www.transfermarkt.es/paris-saint-germain-fc/kader/verein/583/saison_id/2019/plus/1"
source = requests.get(url, headers=headers)
soup = BeautifulSoup(source.content, 'html.parser')

table = soup.find('table', class_="items")

tr = table.find('tr')

tbody = table.find("tbody")

tbody_tr = tbody.find_all("tr")

jugadores = []
posicion = []
fecha_edad = []
pais_nacimiento = []
altura = []
pie = []
fecha_fichado = []
club_anterior = []
fecha_contrato = []
valor_jugador = []
dias_restantes = []

for tr in tbody_tr:
    for td in range(1, len(tr.find_all("td"))):
        if td == 1:
            for td_name in tr.find_all("td")[td].find_all("td", class_="hauptlink"):
                jugadores.append(td_name.find("a").get_text())
                for td_position in tr.find_all('td')[td].find_all('tr')[1:]:
                    posicion.append(td_position.text)

for tr in tbody_tr:
    for td in range(1, len(tr.find_all('td', class_='zentriert'))):
        if td == 1:
            fecha_edad.append(tr.find_all('td', class_='zentriert')[td].text.strip())
        if td == 2:
            pais_nacimiento.append(tr.find_all('td', class_='zentriert')[td].img["title"])
        elif td == 3:
            altura.append(tr.find_all('td', class_='zentriert')[td].text.replace("m", "").strip())
        elif td == 4:
            pie.append(tr.find_all('td', class_='zentriert')[td].text.strip())
        elif td == 5:
            fecha_fichado.append(tr.find_all('td', class_='zentriert')[td].text.strip())
        elif td == 6:
            if tr.find_all('td', class_='zentriert')[td].find('img'):
                club_anterior.append(tr.find_all('td', class_='zentriert')[td].find('img')["alt"])
            else:
                club_anterior.append("-")
        elif td == 7:
            fecha_contrato.append(tr.find_all('td', class_='zentriert')[td].text.strip().replace(".", "/"))
    for td in tr.find_all('td', class_='rechts hauptlink'):
        if "mill" in td.text:
            valor_jugador.append((td.text.split(" ")[0] + "0.000").replace(",", "."))
        elif "miles" in td.text:
            valor_jugador.append(td.text.split(" ")[0] + ".000")
        else:
            valor_jugador.append('-')

for num in range(0, len(fecha_fichado)):
    if fecha_fichado[num] == "-":
        dias_restantes.append("")
    else:
        dias_restantes.append(str((datetime.strptime(fecha_contrato[num].replace("/", "-"), "%d-%m-%Y") - datetime.strptime(fecha_fichado[num].replace("/", "-"), "%d-%m-%Y"))).split(" ")[0])

players_info = pd.DataFrame({
    'jugadores': jugadores,
    'posicion': posicion,
    'nacido/edad': fecha_edad,
    'pais_nacimiento': pais_nacimiento,
    'altura': altura,
    'pie': pie,
    'fichado': fecha_fichado,
    'antes': club_anterior,
    'contrato_hasta': fecha_contrato,
    'dias_restantes': dias_restantes,
    'valor_mercado': valor_jugador
})

players_info.to_csv('players_data.csv')
