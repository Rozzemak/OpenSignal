import uuid
from functools import partial
from typing import List, Any, Set
import io

import numpy
import numpy as np
from bokeh.document.locking import UnlockedDocumentProxy
from bokeh.events import ButtonClick
from bokeh.io import push_notebook
from bokeh.layouts import column, row, layout
from bokeh.model import Model
from bokeh.models.widgets import Select, Button, Slider
from bokeh.document import Document
from bokeh.plotting import figure, output_file, curdoc, show
import fetch_data as fd
import pandas as pd
from Parser import Parser as Pr
from Callbacks import changeGraphCb
from scipy.stats import pearsonr
from OpenGraph import OpenGraph
import base64

from bokeh.models.tools import *
from bokeh.plotting import *
from bokeh.models import CustomJS, LayoutDOM
# create a plot and style its properties
from OpenGraph.OpenGraph import OpenGraph
from bokeh.layouts import row, column, layout
from bokeh.models import ColumnDataSource, CustomJS, HoverTool, PanTool, WheelPanTool, WheelZoomTool, LassoSelectTool, \
    ResetTool, SaveTool, PolySelectTool, ZoomOutTool, ZoomInTool, BoxSelectTool
from bokeh.models.widgets import Button


class OpenSignal:
    openGraph: OpenGraph
    DefaultDoc: List[Model] = []
    Layout: layout() = []


    # OpenGraphSection
    file_source: ColumnDataSource = ""
    activeFile = ""

    def onFileChanged(self, activeFile):
        self.Layout.children = []
        self.Layout.children = [self.createUploadFileButton()]
        self.openGraph = OpenGraph(self.Layout, activeFile)
        # print(self.openGraph.Metadata.Data)
        # print(self.openGraph.Metadata.Data)
        # curdoc().add_root(column(self.controls()))

        # self.modDoc = self.modify_doc(curdoc())

        return ""

    def file_callback(self, attr, old, new):
        raw_contents = new['file_contents'][0]
        # remove the prefix that JS adds
        prefix, b64_contents = raw_contents.split(",", 1)
        file_contents = base64.b64decode(b64_contents)
        print('uploaded: file name:', new['file_name'])
        file_io = io.BytesIO(file_contents)
        df = file_io.read()
        file = df.decode("UTF-8")
        self.activeFile = file
        self.onFileChanged(file)
        return



    def createUploadFileButton(self):
        self.file_source.on_change('data', self.file_callback)
        button = Button(label="Upload", button_type="success", name=str(uuid.uuid1()))
        button.on_click(partial(self.disableButton, button=button))
        #button.on_click(lambda: self.uploadFile(file_source=self.file_source, button=button))
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
        return row(button)

    def disableButton(self, event, button: Button):
        button.label = "Uploading"
        button.disabled = True
        UnlockedDocumentProxy(button.document)\
            .add_next_tick_callback(partial(self.uploadFile, file_source=self.file_source, button=button))

    def uploadFile(self, file_source, button: Button):
        button.label = "Upload"
        button.disabled = False
    ##

    def generateLayout(self):
        return self.Layout

    def __init__(self, document):
        self.openGraph = ""
        self.DefaultDoc = []
        self.activeFile = ""
        self.file_source = ColumnDataSource({'file_contents': [], 'file_name': []})
        self.Layout = layout(self.createUploadFileButton(), [])
        #self.fetch_data = fd.FetchData("https://physionet.org/physiobank/database/emgdb/RECORDS")
        #self.l = self.fetch_data.get_data()
        #self.dfs = Pr.parse_to_csv(self.l)
        #self.fileNames = self.dfs[1]
        #self.load_csv()
        #output_file('dashboard.html')
        #curdoc().add_root(self.createUploadFileButton())
        document.add_root(self.Layout)
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
