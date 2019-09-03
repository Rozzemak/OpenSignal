import sys

import graph
from bokeh.io import push_notebook, show, output_notebook, curdoc, state

from main import mainGraph

doc = curdoc()


def create_document():
    print("docInit")


def on_server_loaded(server_context):
    state.curstate().reset()
    pass


def on_session_created(session_context):
    mainGraph()
    print("session created")
    pass


def cleanup_session(session_context):
    ''' This function is called when a session is closed. '''
    pass


def on_session_destroyed(session_context):

    print("session destroyed")
    ''' If present, this function is called when a session is closed. '''
    #state.curstate().reset()
    pass


#doc.on_session_destroyed(cleanup_session)
