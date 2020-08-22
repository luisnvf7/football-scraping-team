import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

url = "https://www.transfermarkt.es/paris-saint-germain-fc/kader/verein/583/saison_id/2019/plus/1"
source = requests.get(url, headers=headers)
soup = BeautifulSoup(source.content, 'html.parser')

table = soup.find('table', class_="items")

tr = table.find('tr')

players_info = {}

for th in tr.find_all("th")[1:]:
    players_info[th.text] = ""

tbody = table.find("tbody")

tbody_tr = tbody.find_all("tr")

array = []

nombre = ""
edad = ""
nacionalidad = ""
estatura = ""
antes = ""
valor = ""

for tr in tbody_tr:
    for td in tr.find_all("td", class_=True)[1:]:
        if td["class"] == ['posrela']:
            nombre = td.find('a', class_="spielprofil_tooltip").get_text()
        elif td["class"] == ['zentriert'] and ")" in td.text:
            edad = td.text
        elif td.find('img', class_="flaggenrahmen"):
            nacionalidad = td.find('img')["alt"]
        elif td.text.endswith("m"):
            estatura = td.text.replace("m", "").strip()
        elif td.find('a', class_="vereinprofil_tooltip"):
            antes = td.find('img')["alt"]
        elif td["class"] == ["rechts", 'hauptlink']:
            if "mill" in td.text:
                valor = td.text.split(",")
                valor = valor[0] + ".000.000"
            elif "miles" in td.text:
                valor = td.text.split(" ")
                valor = valor[0] + ".000"
            else:
                valor = td.text
            array.append({
                "nombre": nombre,
                "año/edad": edad,
                "nacionalidad": nacionalidad,
                "estatura": estatura,
                "antes": antes,
                "valor": valor
            })

nombres = []
posicion = []

for tr in tbody_tr:
    for td in range(1, len(tr.find_all("td"))):
        if td == 1:
            for td_name in tr.find_all("td")[td].find_all("td", class_="hauptlink"):
                nombres.append(td_name.find("a").get_text())
                for td_position in tr.find_all('td')[td].find_all('tr')[1:]:
                    posicion.append(td_position.text)

for tr in tbody_tr:
    for td in tr.find_all('td', class_='zentriert'):
        print(td.text.strip())
    for td in tr.find_all('td', class_='rechts hauptlink'):
        print(td.text.strip())
        


