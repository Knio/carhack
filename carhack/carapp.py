import os
import time
import logging
import ConfigParser

import tornado.ioloop

import web

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('carapp')

ioloop = tornado.ioloop.IOLoop.instance()


class Singleton(object):
  __instance = None
  def __new__(cls, *args, **kwargs):
    if not cls.__instance:
      i = super(Singleton, cls).__new__(cls, *args, **kwargs)
      cls.__instance = i
    return cls.__instance


class CarApp(Singleton):
  def __init__(self):
    self.config = ConfigParser.ConfigParser()
    self.config.read(['carhack/defaults.ini', 'config.ini'])

    self.data_path = self.config.get('Carhack', 'data_path')
    if not os.path.isdir(self.data_path):
      os.mkdir(self.data_path)

    self.live_trip = None
    self.web = None

    self.trips = {}

  def start_live_trip(self):
    tid = time.strftime('%Y-%m-%d_%H-%M-%S')
    self.live_trip = trip.LiveTrip(tid, os.path.join(self.data_path, tid))
    self.trips[tid] = self.live_trip

  def start_web_server(self):
    web.server.port = self.config.getint('webui', 'port')
    web.init(self)
    web.server.start()

  def load_trips(self):
    for tid in os.listdir(self.data_path):
      path = os.path.join(self.data_path, tid)
      if os.path.isfile(os.path.join(path, trip.CONFIG_NAME)):
        logged_trip = trip.LoggedTrip(tid, path)
        self.trips[tid] = logged_trip

  def run(self):
    self.load_trips()

    if self.config.getboolean('Carhack', 'record_data'):
      self.start_live_trip()

    if self.config.getboolean('Carhack', 'web_interface'):
      self.start_web_server()

    # for windows, since ^C won't interrupt the loop
    tornado.ioloop.PeriodicCallback(lambda:None, 1000).start()

    log.info('Running mainloop. Press Ctrl-C to exit')
    try:
        ioloop.start()
    except KeyboardInterrupt:
        log.info('Exiting')
        self.close()

  def close(self):
    if self.live_trip:
      self.live_trip.close()


app = CarApp()

import trip
