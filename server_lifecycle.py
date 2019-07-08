import sys

import graph
from bokeh.io import push_notebook, show, output_notebook, curdoc, state

from main import mainGraph


def create_document():
    print("docInit")

def on_server_loaded(server_context):
    pass

def on_session_created(session_context):
    mainGraph()
    print("session created")
    pass

def on_session_destroyed(session_context):
    state.curstate().reset()
    print("session destroyed")
    ''' If present, this function is called when a session is closed. '''
    pass




