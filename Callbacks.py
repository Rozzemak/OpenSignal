
from random import random


def SelectPlot(attr, old, new):
    print(attr + " changed from:[" + old + "]to[" + new + "]")
    return 0


def changeGraphCb(attr, old, new):
    SelectPlot(attr, old, new)
    return 0
