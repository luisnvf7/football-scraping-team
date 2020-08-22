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
        elif td == 6:
            if tr.find_all('td', class_='zentriert')[td].find('img'):
                print(tr.find_all('td', class_='zentriert')[td].find('img')["alt"])
            else:
                print("-")
        elif td == 7:
            print(tr.find_all('td', class_='zentriert')[td].text.strip().replace(".", "/"))
        else:
            print(tr.find_all('td', class_='zentriert')[td].text.strip())
    for td in tr.find_all('td', class_='rechts hauptlink'):
        if "mill" in td.text:
            print(td.text.split(",")[0] + ".000.000")
        elif "miles" in td.text:
            print(td.text.split(" ")[0] + ".000")
        print("")

print(str((datetime.strptime("2021-10-5", "%Y-%m-%d") - datetime.strptime("2019-10-5", "%Y-%m-%d"))).split(" ")[0])

print(jugadores)
print(posicion)
print(fecha_edad)
print(pais_nacimiento)
print(altura)
