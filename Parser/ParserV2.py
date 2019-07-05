import configparser as cfg
import io

import pandas as pd
from OpenGraph.Metadata import Metadata
import csv
import requests


def readAscAsMetadata(file: str):
    # Insert default header, header-less throws exc.

    config = cfg.ConfigParser(allow_no_value=True, empty_lines_in_values=False, strict=False)
    fixedFile = ("[top]\n" + file.replace('[COMMENT]', ''))

    config.read_string(fixedFile)
    metadata: Metadata = Metadata()
    metadata.Definitions = dict(config["DEFINITIONS"])
    #  metadata.Comments = config["COMMENT"]
    metadata.SideInfo = set(config["SIDE INFO"])
    metadata.SourceNames = set(config["SOURCE NAMES"])
    metadata.Units = set(config["UNITS"])
    csvFile = (''.join('\n'.join((list(config["DATA"]))))).replace(',', '.')
    metadata.Data = (pd.read_csv(io.StringIO(csvFile), header=None, delimiter='\t'))

    return metadata
