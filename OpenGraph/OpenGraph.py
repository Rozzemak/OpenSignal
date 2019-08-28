import json
from copy import copy, deepcopy
from functools import partial
from os.path import join, dirname
from typing import Type, Set, List

import numpy as np
from bokeh.command.subcommands.json import JSON
from bokeh.layouts import column, row, layout
from bokeh.models import *
from bokeh.models.widgets import Select, Button, Slider
from bokeh.plotting import figure, output_file, curdoc, show, Figure
from isort.utils import union
from numpy import source
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
    CorrCoefRange: RangeSlider = RangeSlider(title="Coeficient limit. (i < corr < j)", start=0.09, end=1,
                                             value=(0.135, 0.95), step=0.0025, format="0.00,0.00")
    DownloadButton = Button(label="Download", button_type="success")
    SimilaritiesSource = ['No similarities found.']

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

            btn = Button(label='Find similarities', button_type='success', width=100, name=str(i))
            btn.on_click(partial(self.calculate_datapoints, graphId=i))
            self.Buttons.append(btn)
            self.Figures.append(plot)

    def createModels(self):
        self.Layout.children.append(layout(row([self.DownloadButton, self.CorrCoefRange])))
        for j in range(len(self.Figures)):
            model = column(self.Buttons[j], self.Figures[j])
            self.Models.append(copy(model))
            self.Layout.children.append(layout(row([self.Figures[j], self.Buttons[j]])))
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

    def calculate_datapoints(self, graphId):
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
        subDataframe = self.Metadata.Data[graphId].iloc[selected[0]: selected[0] + len(selected)]
        # print(list(subDataframe.iloc[:, 0:1]))
        rng = subDataframe.size
        dataFramesDict = {}
        for _graphId in range(len(self.Figures)):
            dataFramesDict[_graphId] = []
            for subGraphId in range(int((self.Metadata.Data[_graphId].size - rng))):
                _list = list(range(subGraphId, subGraphId + rng))
                dataFramesDict[_graphId].append(self.Metadata.Data[_graphId].iloc[_list[0]: _list[0] + len(_list)])
        print("List of correlation ranges created")
        print("Dataframes created")
        print("Dataframecount: " + str(len(dataFramesDict)))
        selectedPointsDict = {}
        CorrelationPasses = {}
        lowerCorrLimit = float(self.CorrCoefRange.value[0])
        uppercorrLimit = float(self.CorrCoefRange.value[1])
        hits: int = 0
        from scipy.stats.stats import pearsonr
        for _dataFrameKey in range(len(dataFramesDict)):
            selectedPointsDict[_dataFrameKey] = []
            CorrelationPasses[_dataFrameKey] = []
            for dataFrameId in range(len(dataFramesDict[_dataFrameKey]) - 1):
                _dtFrame = dataFramesDict[_dataFrameKey][dataFrameId]
                _output = (pearsonr(_dtFrame, subDataframe))
                positiveCoef = _output[0]
                negativeCoef = _output[1]
                # print(output)
                # output = _dtFrame.corr(subDataframe, method='pearson', min_periods=5)
                if (not np.isnan(positiveCoef)) and lowerCorrLimit < positiveCoef < uppercorrLimit \
                        and negativeCoef < 0.05:
                    # < positiveCoef > (negativeCoef - positiveCoef) < negativeCoef:
                    # selectedPointsDict[_dataFrameKey] = union(selectedPointsDict[_dataFrameKey],
                    #                                          _dtFrame.index)
                    CorrelationPasses[_dataFrameKey].extend(list(_dtFrame.index))
                    hits += 1
                    print(_output)
                    # print(str(output)+ "=>" + str(_dtFrame.index[0]))
        print("Correlation mid-step")
        del dataFramesDict
        for _corrPassKey in range(len(CorrelationPasses)):
            CorrelationPasses[_corrPassKey] = sorted(list(set(CorrelationPasses[_corrPassKey])))
        print("Selection points ready")
        for _selectedPointsKey in range(len(CorrelationPasses)):
            self.DataSources[self.Metadata.Definitions["phasename"]][_selectedPointsKey].selected.indices = \
                CorrelationPasses[_selectedPointsKey]
        self.DownloadButton.callback = CustomJS(args=dict(
            source='Signal count:[' + str(len(CorrelationPasses)) + '], Treshold hit count:[' + str(hits)
                   + '](ordered by channel)|->' + json.dumps(CorrelationPasses)),
                                                code=self.DownloadButtonJs())
        del CorrelationPasses
        print("Correlation projection done")
        print("Correlation done")
        return

    # this method is quite namingly unclearly used for visual interpetaion of correlation koef. simmilarity.
    def makePointsSelected(self, corrCheckStart: int, corrCheckStop: int):
        for graphId in range(len(self.Figures)):
            self.DataSources[self.Metadata.Definitions["phasename"]][graphId].selected.indices = union(
                list(range(corrCheckStart, corrCheckStop)),
                list(self.DataSources[self.Metadata.Definitions["phasename"]][graphId].selected.indices))
        return

    def DownloadButtonJs(self):
        return """
function table_to_csv(source) {
    return source
}


const filename = 'data_result.txt'
filetext = table_to_csv(source)
const blob = new Blob([filetext], {type: 'text/plain'})

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename)
} else {
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = filename
    link.target = '_blank'
    link.style.visibility = 'hidden'
    link.dispatchEvent(new MouseEvent('click'))
}
"""
