import pandas as pd
import os
import shutil


def parse_to_csv(file):
    if os.path.isfile("files/" + file+'.csv'):
        os.remove("files/" + file+'.csv')
    df = pd.read_fwf(file)
    df.to_csv(file+'.csv')
    if not os.path.isdir("Files"):
        os.mkdir("Files")
    shutil.move(file+'.csv', "files/" + file+'.csv')
    return df
