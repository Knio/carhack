import json as _json

import decorator
from pyy.web.tornado_simple_server import *


server.add_static_route('^/static/(.*)$', 'web/static')

import page

def init(_app):
    global app
    app = _app
    server.add_static_route('^/static/(.*)$', 'static')

@decorator.decorator
def json(func, *args, **kwargs):
    data = func(*args, **kwargs)
    return _json.dumps(data)

# get_json = lambda u:lambda f:get(u)(f)

@get('^/$')
def index(request):
    return page.CarAppPage()


@get('^/api/trips$')
@json
def trips(request):
    return [trip.to_json() for trip in app.trips.values()]


@get('^/api/trip/(\d[8])$')
@json
def get_series(request, tid):
    trip = app.trips[tid]

    return {
        # 'name':
    }


@get('^/api/trip/([\d\-_]+)/(\w+)/range/(\d+\.\d+)/(\d+\.\d+)$')
@json
def get_range(self, tid, series_name, start_ts, end_ts):
    trip = app.trips[tid]
    series = trip.series[series_name]
    start_ts = float(start_ts)
    end_ts = float(end_ts)
    data = series.get_range(start_ts, end_ts)
    return data
