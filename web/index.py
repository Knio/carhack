from pyy.html import *
from pyy.html.tags import *
from pyy.html.util import *

def main(rh):
    doc = document(title='Carhack!')

    doc.head += script(src='/static/d3.v2.min.js')
    doc.head += script(src='/static/pyy.min.js')

    with doc:
        div('Hello world', id='main')
        script('''wsurl = 'ws://%s/ws';''' % rh.request.host)
        script(include('index.js'))


    return doc
