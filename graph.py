from typing import List, Any, Set
import io

import numpy
import numpy as np
import holoviews as hv
from bokeh.layouts import column, row, layout
from bokeh.model import Model
from bokeh.models.widgets import Select, Button, Slider
from bokeh.plotting import figure, output_file, curdoc, show
import fetch_data as fd
import pandas as pd
from Parser import Parser as Pr
from Callbacks import changeGraphCb
from scipy.stats import pearsonr
from OpenGraph import OpenGraph
import base64

import pandas as pd
from bokeh.models.tools import *
from bokeh.plotting import *
from bokeh.models import CustomJS
# create a plot and style its properties
from OpenGraph.OpenGraph import OpenGraph
from bokeh.layouts import row, column, layout
from bokeh.models import ColumnDataSource, CustomJS, HoverTool, PanTool, WheelPanTool, WheelZoomTool, LassoSelectTool, \
    ResetTool, SaveTool, PolySelectTool, ZoomOutTool, ZoomInTool, BoxSelectTool
from bokeh.models.widgets import Button
from bokeh.io import curdoc
import numpy as np


class OpenSignal:
    openGraph: OpenGraph
    DefaultDoc: List[Model] = []


    # OpenGraphSection
    file_source = ColumnDataSource({'file_contents': [], 'file_name': []})
    activeFile = ""

    def onFileChanged(self):
        self.openGraph = OpenGraph(self.activeFile)
        # print(self.openGraph.Metadata.Data)
        # print(self.openGraph.Metadata.Data)
        # curdoc().add_root(column(self.controls()))

        # self.modDoc = self.modify_doc(curdoc())

        return ""

    def file_callback(self, attr, old, new):
        raw_contents = self.file_source.data['file_contents'][0]
        # remove the prefix that JS adds
        prefix, b64_contents = raw_contents.split(",", 1)
        file_contents = base64.b64decode(b64_contents)
        print('filename:', self.file_source.data['file_name'])
        file_io = io.BytesIO(file_contents)
        df = file_io.read()
        self.activeFile = df.decode("UTF-8")
        self.onFileChanged()
        return ""



    def createUploadFileButton(self):
        self.file_source.on_change('data', self.file_callback)
        button = Button(label="Upload", button_type="success")
        button.callback = CustomJS(args=dict(file_source=self.file_source), code="""
           function read_file(filename) {
               var reader = new FileReader();
               reader.onload = load_handler;
               reader.onerror = error_handler;
               // readAsDataURL represents the file's data as a base64 encoded string
               reader.readAsDataURL(filename);
           }

           function load_handler(event) {
               var b64string = event.target.result;
               file_source.data = {'file_contents' : [b64string], 'file_name':[input.files[0].name]};
               file_source.trigger("change");
           }

           function error_handler(evt) {
               if(evt.target.error.name == "NotReadableError") {
                   alert("Can't read file!");
               }
           }

           var input = document.createElement('input');
           input.setAttribute('type', 'file');
           input.onchange = function(){
               if (window.FileReader) {
                   read_file(input.files[0]);
               } else {
                   alert('FileReader is not supported in this browser');
               }
           }
           input.click();
           """)
        curdoc().add_root(row(button))

    ##

    def __init__(self):
        #self.fetch_data = fd.FetchData("https://physionet.org/physiobank/database/emgdb/RECORDS")
        #self.l = self.fetch_data.get_data()
        #self.dfs = Pr.parse_to_csv(self.l)
        #self.fileNames = self.dfs[1]
        #self.load_csv()
        #output_file('dashboard.html')
        self.createUploadFileButton()
        return


    #  Depreceated down below
    def load_csv(self):
        self.healthy = pd.read_csv("Files/emg_healthy.txt.csv")
        self.myopathy = pd.read_csv("Files/emg_myopathy.txt.csv")
        self.neuropathy = pd.read_csv("Files/emg_neuropathy.txt.csv")
        self.corelate()

    def corelate(self):
        lll = []
        llll = []
        l = self.healthy["x"]
        ll = self.neuropathy["y"]
        lls = self.myopathy["y"]

        for x in range(0, 50):
            lll.append(l[x])
            llll.append(ll[x])

        pear, v_value = pearsonr(lll, llll)
        print(pear)
        return pear

    def controls(self):
        options = self.fileNames
        firstSignal = Select(id=0, title="First signal:", value=options[0], options=options)
        firstSignal.on_change('value', lambda attr, old, new: changeGraphCb(attr, old, new, self.changeGraph, 0))
        secondSignal = Select(id=1, title="Second signal:", value=options[0], options=options)
        secondSignal.on_change('value', lambda attr, old, new: changeGraphCb(attr, old, new, self.changeGraph, 1))

        findButton = Button(label="Find similarities", button_type="success")
        # findButton.on_event(ButtonClick, self.callback)
        # firstSignal.on_change("value", print("value"))
        widgets = column(firstSignal, secondSignal, findButton)
        return widgets

    # To display in a script
    #    doc = modify_doc(curdoc())
