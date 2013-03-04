import json as _json

import decorator
from pyy.web.tornado_simple_server import *


server.add_static_route('^/static/(.*)$', 'carhack/web/static')
server.add_static_route('^/assets/(.*)$', 'carhack/web/assets')

import page

def init(_app):
  global app
  app = _app

@get('^/$')
def index(request):
  return page.CarAppPage()


@decorator.decorator
def json(func, *args, **kwargs):
  data = func(*args, **kwargs)
  return _json.dumps(data)

@get('^/api/trips$')
@json
def trips(request):
  return {tid: trip.to_json() for tid, trip in app.trips.iteritems()}


def encode(x):
  if isinstance(x, (int, float, str, tuple, dict, list)):
    return x
  if hasattr(x, 'tojson'):
    return x.tojson()
  raise Exception(x)

@get('^/api/trip/([\d\-_]+)/([a-zA-Z0-9._]+)/range/(\d+\.?\d*)/(\d+\.?\d*)$')
@json
def get_range(request, tid, series_name, start_ts, end_ts):
  trip = app.trips[tid]
  series = trip.series[series_name]
  start_ts = float(start_ts)
  end_ts = float(end_ts) or None
  data = series.get_range(start_ts, end_ts)
  return data
  # return [(ts, encode(value)) for ts, value in data]


@get('^/api/trip/([\d\-_]+)/recalculate')
@json
def reaclculate(request, tid):
  trip = app.trips[tid]
  trip.recalculate()
  return dict(result='ok')

import logging
import tornado.websocket
log = logging.getLogger('cansocket')
class WebSocket(tornado.websocket.WebSocketHandler):
  def allow_draft76(self):
    return True

  def initialize(self):
    self.names = {}

  def open(self):
    log.info('new connection')

  def on_message(self, message):
    log.info('message: %r', message)
    self.unsubscribe()

    msg = _json.loads(message)
    names = msg.get('series')

    def listener(name):
      def read(ts, value):
        try:
          self.write_message(_json.dumps({'name':name, 'data':[ts, value]}))
        except:
          self.unsubscribe()
      return read

    for name in names:
      func = listener(name)
      self.names[name] = func
      app.live_trip.subscribe(name, func)

  def unsubscribe(self):
    for name, func in self.names.iteritems():
      app.live_trip.unsubscribe(name, func)
    self.names = {}

  def on_close(self):
    log.info('connection closed')
    self.unsubscribe()

add_route('^/api/socket', WebSocket)
