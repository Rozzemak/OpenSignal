from typing import List, Any

from bokeh.layouts import column, row
from bokeh.models.widgets import Select, Button
from bokeh.plotting import figure, output_file, curdoc
import fetch_data as fd
import pandas as pd
from Parser import Parser as Pr
from Callbacks import changeGraphCb


class c_graph:
    fileNames = []
    plots = []

    def __init__(self):
        self.fetch_data = fd.FetchData("https://physionet.org/physiobank/database/emgdb/RECORDS")
        self.l = self.fetch_data.get_data()
        self.dfs = Pr.parse_to_csv(self.l)
        self.fileNames = self.dfs[1]
        output_file('dashboard.html')
        self.load_csv()


    def load_csv(self):
        self.healthy = pd.read_csv("Files/emg_healthy.txt.csv")
        self.myopathy = pd.read_csv("Files/emg_myopathy.txt.csv")
        self.neuropathy = pd.read_csv("Files/emg_neuropathy.txt.csv")

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

    def plotter(self):
        x1 = self.healthy["x"]
        y1 = self.healthy["y"]
        x = [-3, 2, -1, 1]
        y = [-1, 0, -3, 2]

        x2 = self.neuropathy["x"]
        y2 = self.neuropathy["y"]

        plot1 = figure(
            tools="pan,zoom_in,zoom_out",
            title="First signal", width=1200, height=350,
            y_range=(-0.5, 0.5),
            x_range=(1, 1.5)
        )
        plot1.line(x1, y1)

        plot2 = figure(
            title="Second signal", width=1200, height=350,
            y_range=(-0.5, 0.5),
            x_range=(1, 1.5)
        )
        plot2.line(x2, y2)
        plots = column(plot1, plot2)
        self.plots.append(plot1)
        self.plots.append(plot2)
        return plots

    def changeGraph(self, graphId, fileName):
        print("id: [" + str(graphId) + "]["+fileName+"]")


    def run(self):
        curdoc().add_root(row(self.controls(), self.plotter()))

