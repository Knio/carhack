import pyy.html
from pyy.html.tags import *
from pyy.html.util import *

class CarAppPage(pyy.html.document):
  def __init__(self):
    super(CarAppPage, self).__init__('CarHack')

    self.head += link(rel='stylesheet', href='/assets/plok.css', type='text/css')
    self.head += link(rel='stylesheet', href='/assets/normalize.css', type='text/css')

    self.head += script(src='/assets/pyy.js')
    self.head += script(src='/assets/plok.js')
    self.head += script(src='/assets/moment.min.js')

    self.head += script(src='http://ecn.dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=7.0')

    self.head += link(rel='stylesheet', href='/static/carapp.css', type='text/css')

    self.head += script(src='/static/carapp.js')
    self.head += script(src='/static/map.js')

    with self:
      with div():
        h1('CarHack')
        span('Select trip:')

      div(id='carapp')
      script('''window.appui = new CarAppUi('#carapp');''')

