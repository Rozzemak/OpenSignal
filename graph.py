import base64
import io
import uuid
from functools import partial
from typing import List

from bokeh.document.locking import UnlockedDocumentProxy
from bokeh.layouts import row, layout
from bokeh.model import Model
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Button

from OpenGraph import OpenGraph
# create a plot and style its properties
from OpenGraph.OpenGraph import OpenGraph


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
        self.openGraph = OpenGraph(self.Layout, activeFile, self.createUploadFileButton)
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
