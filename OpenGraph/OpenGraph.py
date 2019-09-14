import json
import uuid
from functools import partial
from typing import Dict
from typing import List

import numpy
import numpy as np
from bokeh.document import without_document_lock
from bokeh.document.locking import UnlockedDocumentProxy
from bokeh.events import ButtonClick
from bokeh.layouts import row, layout, layout as lyt
from bokeh.models import *
from bokeh.models.widgets import Button
from bokeh.plotting import figure, curdoc, Figure
from isort.utils import union

from Parser.ParserV2 import readAscAsMetadata
from .Channel import Channel
from .Metadata import Metadata


class OpenGraph:
    Metadata: List[type(Metadata)] = []
    Channels: List[Channel] = [Channel]
    DataSources: Dict[str, List[ColumnDataSource]] = {}
    Figures: List[Figure] = []
    Buttons: List[Button] = []
    ActiveSelection: Dict[int, float] = {}
    Models: List[Column] = []
    Layout: lyt
    CorrCoefRange: RangeSlider = RangeSlider(title="Coeficient limit. (i < corr < j)", start=0.09, end=1,
                                             value=(0.135, 0.95), step=0.0025, format="0.00,0.00",
                                             name=str(uuid.uuid1()))
    DownloadButton: Button = Button(label="Download", button_type="success", name=str(uuid.uuid1()))
    SimilaritiesSource = ['No similarities found.']

    def __init__(self, Layout, AscFile, createUploadFileButton):
        self.Layout = Layout
        self.Curdoc = curdoc
        self.Metadata.append(self.loadFile(AscFile))
        self.Metadata = list(set(self.Metadata))
        self.Layout.children.clear()
        self.Layout.children.append(createUploadFileButton())
        self.Models.clear()
        self.DataSources.clear()
        self.Figures.clear()
        self.Buttons.clear()
        self.ActiveSelection.clear()
        for metadata in self.Metadata:
            print(metadata.Definitions)
            self.loadChannels(metadata)
            self.setDataSources(metadata)
            self.createFigures(metadata)
            self.createModels(metadata)

    def createFigures(self, metadata: Metadata):
        for i in range(len(metadata.Data.columns)):
            y1 = metadata.Data[i].astype(float)
            x1 = np.arange(0, y1.size, 1)

            plot = figure(tools="",
                          title="Channel[" + str(i) + "] Sampling rate[1/" +
                                str(metadata.Definitions["samplingfreq"]) + "]" + " Muscle names[" +
                                str(metadata.SourceNames) + "]",
                          width=1200, height=350,
                          y_range=(metadata.Data[i].min(), metadata.Data[i].max()),
                          x_range=(0, y1.size),
                          name=str(uuid.uuid1())
                          # y_axis_type="datetime", Does not make sence to time this really
                          # x_axis_type="datetime",
                          )
            plot.xaxis.axis_label = "Ticks[Individual samples]"
            plot.yaxis.axis_label = str(list(metadata.Units)[0])

            plot.add_tools(HelpTool(name=str(i) + "pt" + str(uuid.uuid1())))
            plot.add_tools(PanTool(name=str(i) + "pt" + str(uuid.uuid1())))
            plot.add_tools(ZoomInTool(name=str(i) + "zit" + str(uuid.uuid1())))
            plot.add_tools(ZoomOutTool(name=str(i) + "zot" + str(uuid.uuid1())))
            plot.add_tools(BoxSelectTool(name=str(i) + "bst" + str(uuid.uuid1())))
            plot.add_tools(ResetTool(name=str(i) + "rt" + str(uuid.uuid1())))
            plot.add_tools(SaveTool(name=str(i) + "st" + str(uuid.uuid1())))
            plot.line(x1, y1, line_width=1, name=str(i) + str(uuid.uuid1()))

            plot.scatter("xvals", "yvals", source=self.DataSources[metadata.Definitions["phasename"] + metadata.Id][i],
                         alpha=0,
                         selection_color="firebrick", selection_line_alpha=0.1,
                         nonselection_fill_alpha=0.0,
                         name=str(uuid.uuid1())
                         )

            btn = Button(label='Find similarities', button_type='success', width=100, name=str(i) + str(uuid.uuid1()))
            btn.on_event(ButtonClick, partial(self.beforeClicked, button=btn, graphId=i, metadata=metadata))
            self.Buttons.append(btn)
            self.Figures.append(plot)

    def createModels(self, metadata: Metadata):
        self.Layout.children.append(layout(row([self.DownloadButton, self.CorrCoefRange])))
        for j in range(len(self.Figures)):
            model = layout(row([self.Figures[j], self.Buttons[j]]))
            self.Models.append(model)
            self.Layout.children.append(model)
        return

    def setDataSources(self, metadata: Metadata):
        self.DataSources[metadata.Definitions["phasename"] + metadata.Id] = []
        for i in range(len(metadata.Data.columns)):
            y1 = metadata.Data[i].astype(float)
            x1 = np.arange(0, y1.size, 1)
            # todo: add dict to fix ?
            self.DataSources[metadata.Definitions["phasename"] + metadata.Id].append(ColumnDataSource(
                data=dict(
                    xvals=x1,
                    yvals=y1,
                    # letters=[choice(ascii_lowercase) for _ in range(10)]
                )
            ))
        print(self.DataSources)

    @without_document_lock
    def calculate_datapoints(self, graphId: int, button: Button, metadata: Metadata):
        # Thread(target=lambda: UnlockedDocumentProxy(button.document).add_next_tick_callback()).start()
        self.threadCorelate(graphId, button, metadata)
        button.label = 'Find Similarities'
        button.disabled = False
        # thread.join()
        # button.label = "Done!"
        # for child in self.Layout.children:
        #    if type(child) is Row:
        #        for btn in child.children:
        #            if type(btn) is Button:
        #                print("d")
        #                btn.label = ''
        # self.DownloadButton.label = "aa"
        # self.Layout.u
        # print(list(itertools.chain.from_iterable(self.Layout)))

        # for btn in self.Buttons:
        #    btn.label = "duh"  # WTF, this dus not work!! todo: report the whack out of this to git

    def threadCorelate(self, graphId: int, button: Button, metadata: Metadata):
        indices = self.DataSources[metadata.Definitions["phasename"]+ metadata.Id][graphId].selected.indices
        self.ActiveSelection = dict(zip(sorted(list(indices)),
                                        metadata.Data[graphId].astype(float)))
        self.iterateAndCorrelate(graphId, sorted(list(indices)), button, metadata)
        # for btn in self.Buttons:

    def beforeClicked(self, event, button: Button, graphId: int, metadata: Metadata):
        button.disabled = True
        button.label = 'Working!'
        UnlockedDocumentProxy(button.document).add_next_tick_callback(
            partial(self.calculate_datapoints, graphId=graphId, button=button, metadata=metadata))

    def loadFile(self, fileStream):
        return readAscAsMetadata(fileStream)

    def loadChannels(self, metadata: Metadata):
        for _ in range(int(metadata.Definitions["channelcount"])):
            self.Channels.append(Channel(metadata.Definitions["datatype"],
                                         metadata.Definitions["samplingfreq"],
                                         metadata.Definitions["firstsampletime"], metadata.Data))

    def iterateAndCorrelate(self, graphId, selected, button: Button, metadata: Metadata):
        if len(selected) < 2:
            return
        subDataframe = metadata.Data[graphId].iloc[selected[0]: selected[0] + len(selected)]
        # print(list(subDataframe.iloc[:, 0:1]))
        rng = subDataframe.size
        dataFramesDict = {}
        CorrelationPasses = {}
        for _graphId in range(len(self.Figures)):
            print(_graphId)
            dataFramesDict[_graphId] = []
            CorrelationPasses[str(_graphId) + metadata.Id] = []
            # todo: callback, will crash here on multiple files
            UnlockedDocumentProxy(button.document).add_next_tick_callback(
                partial(self.progressReport, progressValue=_graphId, button=button))
            for subGraphId in range(int((metadata.Data[_graphId].size - rng))):
                _list = list(range(subGraphId, subGraphId + rng))
                dataFramesDict[_graphId].append(metadata.Data[_graphId].iloc[_list[0]:
                                                                                  numpy.clip(_list[0] + len(_list), 0,
                                                                                             metadata.Data[
                                                                                                 _graphId].size)])
                del _list
        print("List of correlation ranges created")
        print("Dataframes created")
        print("Dataframecount: " + str(len(dataFramesDict)))
        selectedPointsDict = {}
        lowerCorrLimit = float(self.CorrCoefRange.value[0])
        uppercorrLimit = float(self.CorrCoefRange.value[1])
        hits: int = 0
        from scipy.stats.stats import pearsonr
        for _dataFrameKey in range(len(dataFramesDict)):
            selectedPointsDict[_dataFrameKey] = []
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
                    lst = list(_dtFrame.index)
                    # todo: is out of bounds for multiple files. _id is > than source names
                    # CorrelationPasses[str(list(metadata.SourceNames)[_dataFrameKey]) + metadata.Id].extend(lst)
                    CorrelationPasses[str(_dataFrameKey) + metadata.Id].extend(lst)
                    del lst
                    hits += 1
                    print(_output)
                    # print(str(output)+ "=>" + str(_dtFrame.index[0]))
        print("Correlation mid-step")
        del dataFramesDict
        for _corrPassKey in CorrelationPasses:
            CorrelationPasses[_corrPassKey] = sorted(list(set(CorrelationPasses[_corrPassKey])))
        print("Selection points ready")
        for _selectedPointsKey in CorrelationPasses:
            self.DataSources[metadata.Definitions["phasename"] + metadata.Id][
                list(CorrelationPasses.keys()).index(_selectedPointsKey)].selected.indices = \
                CorrelationPasses[_selectedPointsKey]
        self.DownloadButton.callback = CustomJS(args=dict(
            source='Signal count:[' + str(len(CorrelationPasses)) + '], Treshold hit count:[' + str(hits)
                   + '] Compared to:(channel:[' + str(list(metadata.SourceNames)[graphId]) + '],'
                   + 'channel:[' + str(graphId) + '],'
                   + ')data:{' + str(list(subDataframe)) + '}(ordered by channel)|->' + json.dumps(CorrelationPasses)),
            code=self.DownloadButtonJs())
        del CorrelationPasses
        print("Correlation projection done")
        print("Correlation done")
        return

    # this method is quite namingly unclearly used for visual interpetaion of correlation koef. simmilarity.
    # deprecated
    def makePointsSelected(self, corrCheckStart: int, corrCheckStop: int, metadata: Metadata):
        for graphId in range(len(self.Figures)):
            # todo: fix datasources
            self.DataSources[metadata.Definitions["phasename"] + metadata.Id][graphId].selected.indices = union(
                list(range(corrCheckStart, corrCheckStop)),
                list(self.DataSources[metadata.Definitions["phasename"] + metadata.Id][graphId].selected.indices))
        return

    def progressReport(self, button: Button, progressValue):
        button.label = str(progressValue)
        return

    def DownloadButtonJs(self):
        return """
function downloadFile(source) {
    return source
}

const filename = 'data_result.txt'
filetext = downloadFile(source)
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
