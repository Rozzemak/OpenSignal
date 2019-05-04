from typing import List, Any

from bokeh.layouts import column, row
from bokeh.models.widgets import Select, Button
from bokeh.plotting import figure, output_file, curdoc
import fetch_data as fd
import pandas as pd
from Parser import Parser as Pr
from Callbacks import changeGraphCb
from scipy.stats import pearsonr


class c_graph:
    fileNames = []
    plots = []
    plotArgs = []
    plotDict = {}

    def __init__(self):
        self.fetch_data = fd.FetchData("https://physionet.org/physiobank/database/emgdb/RECORDS")
        self.l = self.fetch_data.get_data()
        self.dfs = Pr.parse_to_csv(self.l)
        self.fileNames = self.dfs[1]
        self.load_csv()
        output_file('dashboard.html')
        curdoc().add_root(column(self.controls()))
        curdoc().add_root(row(self.changeGraph(-1, "emg_healthy.txt.csv")))


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
        firstSignal.on_change('value', lambda attr, old, new : changeGraphCb(attr, old, new, self.changeGraph, 0))
        secondSignal = Select(id=1, title="Second signal:", value=options[0], options=options)
        secondSignal.on_change('value', lambda attr, old, new : changeGraphCb(attr, old, new, self.changeGraph, 1))

        findButton = Button(label="Find similarities", button_type="success")
        #findButton.on_event(ButtonClick, self.callback)
        #firstSignal.on_change("value", print("value"))
        widgets = column(firstSignal, secondSignal, findButton)
        return widgets

    def createPlots(self, graph, filename):
        x1 = graph["x"]
        y1 = graph["y"]

        plot1 = figure(
            tools="pan,zoom_in,zoom_out",
            title="First signal", width=1200, height=350,
            y_range=(-0.5, 0.5),
            x_range=(1, 1.5)
        )
        plot1.line(x1, y1)
        self.plotDict[filename] = plot1
        return plot1

    oldGraphId = -1
    def changeGraph(self, graphId, fileName, oldFileName=-1):
        print("id: [" + str(graphId) + "]["+fileName+"]")
        #self.plotter(self.healthy)
        #self.plotter(self.myopathy)
        print(self.plotDict)
        self.plotDict[fileName] = self.createPlots(pd.read_csv("Files/"+fileName), fileName)
        print(self.plotDict[fileName])
        if not oldFileName == -1:
            #and not graphId != self.oldGraphId:
            curdoc().remove_root(self.plotDict[oldFileName])
        curdoc().add_root(self.plotDict[fileName])
        self.oldGraphId = graphId



    def run(self):
        return 0

