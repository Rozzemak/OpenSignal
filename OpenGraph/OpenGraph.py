from functools import partial
from typing import Type, Set, List

import numpy as np
import holoviews as hv
from bokeh.layouts import column, row, layout
from bokeh.models import *
from bokeh.models.widgets import Select, Button, Slider
from bokeh.plotting import figure, output_file, curdoc, show, Figure
from numpy import source

import fetch_data as fd
import pandas as pd

from OpenGraph.Channel import Channel
from OpenGraph.Metadata import Metadata
from Parser import Parser as Pr
from Callbacks import changeGraphCb
from scipy.stats import pearsonr
from typing import Dict
from .Metadata import Metadata
from .Channel import Channel
from Parser.ParserV2 import readAscAsMetadata


class OpenGraph:
    Metadata: Metadata
    Channels: List[Channel] = [Channel]
    DataSources: List[ColumnDataSource] = []
    Figures: List[Figure] = []
    Buttons: List[Button] = []
    ActiveSelection: Dict[int, float] = {}


    def __init__(self, AscFile):
        self.Metadata = self.loadFile(AscFile)
        print(self.Metadata.Definitions)
        self.loadChannels()
        self.setDataSources()
        self.createFigures()

    def createFigures(self):
        for i in range(len(self.Metadata.Data.columns)):
            y1 = self.Metadata.Data[i].astype(float)
            x1 = np.arange(0, y1.size, 1)

            plot = figure(
                tools=[PanTool(), ZoomOutTool(), ZoomInTool(),
                       BoxSelectTool(), ResetTool(), SaveTool()],
                title="Channel[" + str(i) + "] Sampl. freq[1/" +
                      str(self.Metadata.Definitions["samplingfreq"]) + "]" + " Muscle names[" +
                      str(self.Metadata.SourceNames)+"]",
                width=1200, height=350,
                y_range=(self.Metadata.Data[i].min(), self.Metadata.Data[i].max()),
                x_range=(0, y1.size),
                x_axis_label="Ticks[Sampling Rate]",
                y_axis_label=str(list(self.Metadata.Units)[0]),
                x_axis_location="below"
                #y_axis_type="datetime", Does not make sence to time this really
                #x_axis_type="datetime",
                )

            plot.line(x1, y1, line_width=1)
            plot.scatter("xvals", "yvals", source=self.DataSources[i],
                         alpha=0,
                         selection_color="firebrick", selection_line_alpha=0.1)

            btn = Button(label='Selected points', button_type='success', name=str(i))
            print(i)
            btn.on_click(partial(self.print_datapoints, graphId=i))
            self.Buttons.append(btn)
            self.Figures.append(plot)

    def setDataSources(self):
        for i in range(len(self.Metadata.Data.columns)):
            y1 = self.Metadata.Data[i].astype(float)
            x1 = np.arange(0, y1.size, 1)
            self.DataSources.append(ColumnDataSource(
                data=dict(
                    xvals=x1,
                    yvals=y1,
                    #letters=[choice(ascii_lowercase) for _ in range(10)]
                )
            ))

    def print_datapoints(self, graphId):
        indices = self.DataSources[graphId].selected.indices
        self.ActiveSelection = dict(zip(sorted(list(indices)),
                                        self.Metadata.Data[graphId].astype(float)))
        print(self.ActiveSelection)


    def loadFile(self, fileStream):
        return readAscAsMetadata(fileStream)

    def loadChannels(self):
        for _ in range(int(self.Metadata.Definitions["channelcount"])):
            self.Channels.append(Channel(self.Metadata.Definitions["datatype"],
                                         self.Metadata.Definitions["samplingfreq"],
                                         self.Metadata.Definitions["firstsampletime"], self.Metadata.Data))
