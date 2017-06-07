import requests
import xmltodict
import bs4
from bs4 import BeautifulSoup



def clean_message(message):
    message = message.replace('<STRONG>', '')
    message = message.replace('</STRONG>', '')
    soup = BeautifulSoup(message, 'html.parser')
    cleaned_message = ''.join([x for x in soup.contents if type(x) == bs4.element.NavigableString])
    return cleaned_message


def get_line_status(line):
    r = requests.get('http://web.mta.info/status/serviceStatus.txt')
    status = r.text
    xml = xmltodict.parse(status)
    subway_service = xml['service']['subway']['line']

    line_index = {'1': 0, '2': 0, '3': 0,
                  '4': 1, '5': 1, '6': 1, '7': 2, 
                  'A': 3, 'C': 3, 'E': 3,
                  'B': 4, 'D': 4, 'F': 4, 'M': 4,
                  'G': 5, 'J': 6, 'Z': 6, 'L': 7,
                  'N': 8, 'Q': 8, 'R': 8, 'S': 9}

    try:
        info = subway_service[line_index[line]]
    except KeyError:
        return '', ''
    
    status = info['status']
    if status == 'DELAYS':
        text = clean_message(info['text'])
        if '[{}]'.format(line) in text:
            return status, text
        else:
            return 'GOOD SERVICE', ''
    else:
        return 'GOOD SERVICE', ''

def citi_bikes():
    station_map = {'3456': 'Schermerhorn & 3rd',
                   '395': 'Schermerhorn & Bond',
                   '3232': 'Bond & Fulton',
                   '324': 'Dekalb & Hudson'}

    r = requests.get('https://gbfs.citibikenyc.com/gbfs/en/station_status.json').json()

    stations = [x for x in r['data']['stations'] if x['station_id'] in station_map.keys()]

    results = []
    for station in stations:
        results.append((station_map[station['station_id']], station['num_bikes_available']))

    return results


