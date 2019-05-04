from bokeh.models.callbacks import CustomJS
from bokeh.layouts import grid, column, row
from bokeh.models.widgets import Select, Button
from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.events import ButtonClick
import fetch_data as fd
import pandas as pd
from Parser import Parser as Pr


class c_graph:
    def __init__(self):
        self.fetch_data = fd.FetchData("https://physionet.org/physiobank/database/emgdb/RECORDS")
        self.l = self.fetch_data.get_data()
        self.dfs = Pr.parse_to_csv(self.l)
        output_file('dashboard.html')
        self.load_csv()


    def load_csv(self):
        self.healthy = pd.read_csv("Files/emg_healthy.txt.csv")
        self.myopathy = pd.read_csv("Files/emg_myopathy.txt.csv")
        self.neuropathy = pd.read_csv("Files/emg_neuropathy.txt.csv")

    def controls(self):
        options = ["Healthy", "Myopathy", "Neurophaty"]
        firstSignal = Select(title="First signal:", options=options)
        secondSignal = Select(title="Second signal:", options=options)
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

        x2 = [-5, 3, -2, 1]
        y2 = [-4, 4, -2, 1]

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
        return plots

    def run(self):
        curdoc().add_root(row(self.controls(), self.plotter()))

