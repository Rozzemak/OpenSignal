from typing import Dict, Union, List, Any

from pandas import DataFrame

from OpenGraph.ChannelData import ChannelData


class Metadata:
    #  Im gonna keep these meta definitions here just as deafults
    Definitions: Dict[str, Union[int, float, str]]
    Comments: Dict[str, str] = {"Comment1": ""}
    SourceNames: List[str]  # Name ForEach channel
    SideInfo: List[str]  # NoIdea, maybe like muscle-side
    Units: List[str]  # Just units (volts)
    Data: DataFrame  # Actual data, gonna put this in metadata anyway

    def __init__(self):
        return



