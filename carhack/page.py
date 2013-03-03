import pyy.html
from pyy.html.tags import *
from pyy.html.util import *

class CarAppPage(pyy.html.document):
  def __init__(self):
    super(CarAppPage, self).__init__('CarHack')

    self.head += link(rel='stylesheet', href='/assets/plok.css', type='terxt/css')
    self.head += link(rel='stylesheet', href='/assets/normalize.css', type='terxt/css')

    self.head += script(src='/assets/pyy.js')
    self.head += script(src='/assets/plok.js')
    self.head += script(src='/assets/moment.min.js')

    self.head += link(rel='stylesheet', href='/static/carapp.css', type='terxt/css')

    self.head += script(src='/static/carapp.js')

    with self:
      with div():
        h1('CarHack')
        span('Select trip:')

      div(id='carapp')
      script('''window.appui = new CarAppUi('#carapp');''')

