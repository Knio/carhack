from pyy.html import *
from pyy.html.tags import *
from pyy.html.util import *

def index(rh):
    doc = document(title='Carhack!')

    doc.head += script(src='/static/d3.v2.min.js')
    doc.head += script(src='/static/pyy.min.js')
    # doc.head += script(src='https://raw.github.com/Knio/pyy.js/master/pyy.min.js')

    doc.head += link(rel='stylesheet', href='/static/style.css')
    with doc:

        div(id='cam')
        div(id='data')
        div(id='frames')

        script('''wsurl = 'ws://%s/';''' % rh.request.host)
        script(include('web/graph.js'))
        script(include('web/index.js'))


    return doc
