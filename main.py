from bokeh.application import Application

from bokeh.client import pull_session
from bokeh.embed import server_session
from bokeh.embed import autoload_static

from bokeh.document import Document
from bokeh.io import curdoc, reset_output, state
from bokeh.io.doc import set_curdoc

import graph


# graph.OpenSignal(curdoc())

def mainGraph():
    #doc = Document()
    #set_curdoc(doc)
    #doc = curdoc()
    #doc: Document
    #if graph is  graph
    #doc.remove_root(doc.roots)
    #curdoc().clear()
    #graph.reset_output()
    graph.OpenSignal(curdoc())

    return


mainGraph()
