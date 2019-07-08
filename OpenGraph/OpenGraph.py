from copy import copy, deepcopy
from functools import partial
from typing import Type, Set, List

import numpy as np
import holoviews as hv
from bokeh.layouts import column, row, layout
from bokeh.models import *
from bokeh.models.widgets import Select, Button, Slider
from bokeh.plotting import figure, output_file, curdoc, show, Figure
from isort.utils import union
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
    DataSources: Dict[str, List[ColumnDataSource]] = {}
    Figures: List[Figure] = []
    Buttons: List[Button] = []
    ActiveSelection: Dict[int, float] = {}
    Models: List[Column] = []
    Layout: layout

    def __init__(self, Layout, AscFile):
        self.Layout = Layout
        self.Curdoc = curdoc
        self.Metadata = self.loadFile(AscFile)
        print(self.Metadata.Definitions)
        self.loadChannels()
        self.setDataSources()
        self.createFigures()
        self.createModels()

    def createFigures(self):
        for i in range(len(self.Metadata.Data.columns)):
            y1 = self.Metadata.Data[i].astype(float)
            x1 = np.arange(0, y1.size, 1)

            plot = figure(tools="",
                          title="Channel[" + str(i) + "] Sampling rate[1/" +
                                str(self.Metadata.Definitions["samplingfreq"]) + "]" + " Muscle names[" +
                                str(self.Metadata.SourceNames) + "]",
                          width=1200, height=350,
                          y_range=(self.Metadata.Data[i].min(), self.Metadata.Data[i].max()),
                          x_range=(0, y1.size),
                          # y_axis_type="datetime", Does not make sence to time this really
                          # x_axis_type="datetime",
                          )
            plot.xaxis.axis_label = "Ticks[Individual samples]"
            plot.yaxis.axis_label = str(list(self.Metadata.Units)[0])

            plot.add_tools(HelpTool(name=str(i) + "pt"))
            plot.add_tools(PanTool(name=str(i) + "pt"))
            plot.add_tools(ZoomInTool(name=str(i) + "zit"))
            plot.add_tools(ZoomOutTool(name=str(i) + "zot"))
            plot.add_tools(BoxSelectTool(name=str(i) + "bst"))
            plot.add_tools(ResetTool(name=str(i) + "rt"))
            plot.add_tools(SaveTool(name=str(i) + "st"))
            plot.line(x1, y1, line_width=1, name=str(i))

            plot.scatter("xvals", "yvals", source=self.DataSources[self.Metadata.Definitions["phasename"]][i],
                         alpha=0,
                         selection_color="firebrick", selection_line_alpha=0.1,
                         nonselection_fill_alpha=0.0
                         )

            btn = Button(label='Selected points', button_type='success', name=str(i))
            btn.on_click(partial(self.print_datapoints, graphId=i))
            self.Buttons.append(btn)
            self.Figures.append(plot)

    def createModels(self):
        for j in range(len(self.Figures)):
            model = column(self.Buttons[j], self.Figures[j])
            self.Models.append(copy(model))
            self.Layout.children.append(layout([self.Buttons[j], self.Figures[j]]))
        return

    def setDataSources(self):
        self.DataSources[self.Metadata.Definitions["phasename"]] = []
        for i in range(len(self.Metadata.Data.columns)):
            y1 = self.Metadata.Data[i].astype(float)
            x1 = np.arange(0, y1.size, 1)

            self.DataSources[self.Metadata.Definitions["phasename"]].append(ColumnDataSource(
                data=dict(
                    xvals=x1,
                    yvals=y1,
                    # letters=[choice(ascii_lowercase) for _ in range(10)]
                )
            ))
        print(self.DataSources)

    def print_datapoints(self, graphId):
        indices = self.DataSources[self.Metadata.Definitions["phasename"]][graphId].selected.indices
        self.ActiveSelection = dict(zip(sorted(list(indices)),
                                        self.Metadata.Data[graphId].astype(float)))
        # print(self.ActiveSelection)
        # print(self.Metadata.Data[0].corr(self.Metadata.Data[1], method='pearson', min_periods=1))
        # self.makePointsSelected(1, 5000)
        self.iterateAndCorrelate(graphId, sorted(list(indices)))

    def loadFile(self, fileStream):
        return readAscAsMetadata(fileStream)

    def loadChannels(self):
        for _ in range(int(self.Metadata.Definitions["channelcount"])):
            self.Channels.append(Channel(self.Metadata.Definitions["datatype"],
                                         self.Metadata.Definitions["samplingfreq"],
                                         self.Metadata.Definitions["firstsampletime"], self.Metadata.Data))

    def iterateAndCorrelate(self, graphId, selected):
        from pandas import DataFrame
        subDataframe = self.Metadata.Data[graphId].iloc[selected[0]: selected[0] + len(selected)]
        rng = subDataframe.size
        ilocSelection = {}
        ilocDataFrames = []
        for _graphId in range(len(self.Figures)):
            ilocSelection[_graphId] = []
            for subGraphId in range(int((self.Metadata.Data[_graphId].size - rng))):
                ilocSelection[_graphId] += [list(range(subGraphId, subGraphId + rng))]
        print("List of correlation ranges created")
        dataFrames = []
        for _graphId in range(len(self.Figures)):
            for sublist in range(len(ilocSelection[_graphId]) - rng):
                _list = ilocSelection[_graphId][sublist]
                dataFrames.append(self.Metadata.Data[_graphId].iloc[_list[0]: _list[0] + len(_list)])
        del ilocSelection
        print("Dataframes created")
        for _dataFrame in range(len(dataFrames)):
            output = dataFrames[_dataFrame].corr(subDataframe, method='spearman')
            if (not np.isnan(output)) and abs(output) > 0.3:
                #self.makePointsSelected(int(dataFrames[_dataFrame].iloc[0]), dataFrames[_dataFrame].size)
                print(output)

        #        output = self.Metadata.Data[_graphId].iloc[ilocSelection[_graphId][sublist]].corr(
        #            subDataframe, method='kendall', min_periods=1)
        #        # for _graphId in range(len(self.Figures)):
        #        # output = self.Metadata.Data[_graphId].iloc[ilocSelection[_graphId]].corr(
        #        # subDataframe, method='kendall', min_periods=1)
        #        # if abs(output) > 0.7:
        #        # self.makePointsSelected(subGraphId, subGraphId + rng)
        #        #  print(str(output) + "["+str(subGraphId)+"=>" + str((subGraphId)+rng)+"]")
        #        print(output)

        # print(subDataframe.corr(subDataframe,method='kendall'))

        # print(subDataframe)
        # print(self.Metadata.Data[graphId].iloc[selected[0]: selected[0] + len(selected)].corr(
        #    self.Metadata.Data[1].iloc[selected[0]: selected[0] + len(selected)], method='pearson', min_periods=1))
        print("Correlation done")
        return

    # this method is quite namingly unclearly used for visual interpetaion of correlation koef. simmilarity.
    def makePointsSelected(self, corrCheckStart: int, corrCheckStop: int):
        for graphId in range(len(self.Figures)):
            self.DataSources[self.Metadata.Definitions["phasename"]][graphId].selected.indices = union(
                list(range(corrCheckStart, corrCheckStop)),
                list(self.DataSources[self.Metadata.Definitions["phasename"]][graphId].selected.indices))
        return
