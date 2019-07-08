from bokeh.application import Application
from flask import Flask, render_template

from bokeh.client import pull_session
from bokeh.embed import server_session
from bokeh.embed import autoload_static


from bokeh.document import Document
from bokeh.io import curdoc, reset_output, state
from bokeh.io.doc import set_curdoc

import graph

graph.OpenSignal(curdoc())

def mainGraph():
    #set_curdoc(Document())
    #graph.OpenSignal()

    return

