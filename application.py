from flask import (Flask, request, render_template, session, 
    redirect, url_for, escape, flash, abort, jsonify)

from application import gm
from application import morning

application = Flask(__name__)
application.config.from_pyfile('config.cfg')

@application.route('/')
def index():
    return 'Hello world'

@application.route('/transit')
def transit():
    HOME = '40.687305, -73.981217'
    VICE = '40.702192, -73.989690'
    KOHLS = '40.753088, -73.986701'
    vice = gm.get_transit_times(HOME, VICE)
    kohls = gm.get_transit_times(HOME, KOHLS)
    citibike = morning.citi_bikes()
    return render_template('index.html', vice=vice, kohls=kohls, cb=citibike)

@application.route('/update')
def update_tables():
    HOME = '40.687305, -73.981217'
    VICE = '40.702192, -73.989690'
    KOHLS = '40.753088, -73.986701'
    vice = gm.get_transit_times(HOME, VICE)
    kohls = gm.get_transit_times(HOME, KOHLS)
    citibike = morning.citi_bikes()
    return jsonify({'vice': vice, 'kohls': kohls, 'citibike': citibike})


if __name__ == '__main__':
    application.run(host='0.0.0.0')