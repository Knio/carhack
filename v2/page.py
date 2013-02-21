import pyy.html
from pyy.html.tags import *
from pyy.html.util import *

class CarAppPage(pyy.html.document):
  def __init__(self):
    super(CarAppPage, self).__init__('CarHack')

    self.head += link(rel='stylesheet', href='http://plok.zkpq.ca/plok.css', type='terxt/css')

    self.head += script(src='http://pyy.zkpq.ca/pyy.js')
    self.head += script(src='http://plok.zkpq.ca/plok.js')

    self.head += script(src='/static/carapp.js')

    with self:
      script('''carapp.load();''')
      with div():
        h1('CarHack')
        a('View trips', href='/api/trips')


