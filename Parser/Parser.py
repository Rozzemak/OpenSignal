import pandas as pd
import os
import shutil


def parse_to_csv(data):
    for x in data:
        open(str(x)+'.txt', 'wb').write(data[x].read())
        parse_to_csv_local(str(x)+'.txt')
    for x in data:
        os.remove(str(x)+'.txt')
    return 0


def parse_to_csv_local(file):
    if os.path.isfile("files/" + file+'.csv'):
        os.remove("files/" + file+'.csv')
    df = pd.read_fwf(file)
    df.to_csv(file+'.csv')
    if not os.path.isdir("Files"):
        os.mkdir("Files")
    shutil.move(file+'.csv', "files/" + file+'.csv')
    return df
