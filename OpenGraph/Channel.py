from typing import Type, List

from pandas import DataFrame


class Channel:
    DataType: int
    SamplingFreq: float
    FirstSampleTime: float
    ChannelData: List[float]
    
    def __init__(self, dataType: int, samplingFreq: float, firstSampleTime: float, channelData: List[float]) -> object:
        """

        :rtype: Channel
        """
        self.FirstSampleTime = firstSampleTime
        self.SamplingFreq = samplingFreq
        self.DataType = dataType
        self.ChannelData = channelData


