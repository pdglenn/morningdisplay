from flask import current_app as application
from googlemaps import Client
from . import morning
import os

def get_transit_times(origin, destination):
    key = application.config['GOOGLE_MAPS']
    c = Client(key)
    d = c.directions(origin, destination, mode='transit', alternatives=True)

    results = set()
    for route in d:
        duration = route['legs'][0]['duration']['text']
        steps = route['legs'][0]['steps']
        transit_details = [x for x in steps if x.get('travel_mode') == 'TRANSIT'][0]['transit_details']
        depart_stop = transit_details['departure_stop']['name']
        depart_stop = depart_stop.replace('Subway', '')
        depart_stop = depart_stop.replace('Station', '')
        depart_stop = depart_stop.replace('Atlantic Avenue', '')
        line = transit_details['line']['short_name']
        try:
            icon = transit_details['line']['icon']
        except KeyError:
            icon = transit_details['line']['vehicle']['icon']

        status, text = morning.get_line_status(line)
        icon_html = '<img src="{}">'.format(icon)
        # results.add((line, depart_stop, duration, icon, status, text))
        results.add((icon_html, depart_stop, duration, status, text))
    return sorted(list(results), key=lambda x: x[2])





