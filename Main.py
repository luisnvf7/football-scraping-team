import requests
from bs4 import BeautifulSoup

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

for tr in tbody_tr:
    for td in tr.find_all("td", class_=True)[1:]:
        if td["class"] == ['posrela']:
            table_td = td.find('table', class_="inline-table")
            for tbody in table_td.find_all('tr'):


