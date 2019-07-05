import io
from random import random
import bokeh.colors
from bokeh.colors import color
from bokeh.palettes import *
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.plotting import figure, curdoc
from bokeh.palettes import RdYlBu3 as palette  # @UnresolvedImport

from bokeh.layouts import row
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Button
from bokeh.io import curdoc
import numpy as np

import base64

import pandas as pd

# create a plot and style its properties
from OpenGraph.OpenGraph import OpenGraph

p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None

# add a text renderer to our plot (no data yet)
r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
           text_baseline="middle", text_align="center")

i = 0



ds = r.data_source


# o = OpenGraph("FL-EXT zapesti.ASC")

# create a callback that will add a number in a random location
def callback():
    global i

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['x'] = ds.data['x'] + [random() * 70 + 15]
    new_data['y'] = ds.data['y'] + [random() * 70 + 15]
    new_data['text_color'] = ds.data['text_color'] + [palette[i % 3]]
    new_data['text'] = ds.data['text'] + [str(i)]
    ds.data = new_data

    i = i + 1


# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))
