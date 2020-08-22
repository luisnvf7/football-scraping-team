import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

url = "https://www.transfermarkt.es/paris-saint-germain-fc/kader/verein/583/saison_id/2019/plus/1"
source = requests.get(url, headers=headers)
soup = BeautifulSoup(source.content, 'html.parser')

table = soup.find('table', class_='items')

tbody_table = table.find('tbody')

for td in tbody_table.find_all('td'):
    

for tr in tbody_tr:
    for td in range(1, len(tr.find_all("td"))):
        if td == 1:
            for td_name in tr.find_all("td")[td].find_all("td", class_="hauptlink"):
                nombres.append(td_name.find("a").get_text())

print(nombres)