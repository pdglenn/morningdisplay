import requests
import xmltodict
import bs4
from bs4 import BeautifulSoup

station_map = {'3456': 'Schermerhorn & 3rd',
               '395': 'Schermerhorn & Bond',
               '3232': 'Bond & Fulton',
               '324': 'Dekalb & Hudson'}

r = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json').json()
print(r)
stations = [x for x in r if x['station_id'] in station_map.keys()]

results = []
for station in stations:
    results.append((station_map[station['station_id']], station['num_bikes_available']))