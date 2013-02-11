import json as _json

import decorator

from pyy.web.tornado_simple_server import *

def init(_carhack):
    global carhack
    carhack = _carhack
    server.add_static_route('^/static/(.*)$', 'static')

@decorator.decorator
def json(func, *args, **kwargs):
    data = func(*args, **kwargs)
    return _json.dumps(data)

# get_json = lambda u:lambda f:get(u)(f)

@get('^/$')
def index(request):
    return 'Hello world'

@get('^/api/trips$')
@json
def trips(request):
    return sorted([trip.name for trip in carhack.trips])


@get('^/api/trip/(\d[8])$')
@json
def get_trip(request, tid):
    trip = carhack.trips[tid]

    return {
        # 'name':
    }
