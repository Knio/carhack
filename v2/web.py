import json as _json

import decorator
from pyy.web.tornado_simple_server import *

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
    return sorted([dict(tid=tid, name=t.name) for tid,t in app.trips.items()])


@get('^/api/trip/(\d[8])$')
@json
def get_trip(request, tid):
    trip = app.trips[tid]

    return {
        # 'name':
    }
