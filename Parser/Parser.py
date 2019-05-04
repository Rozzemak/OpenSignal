import pandas as pd
import os
import shutil


def parse_to_csv(data):
    df = []
    for x in data:
        open(str(x)+'.txt', 'wb').write(data[x].read())
        df.append(parse_to_csv_local(str(x)+'.txt'))
    for x in data:
        os.remove(str(x)+'.txt')
    return df


def parse_to_csv_local(file):
    if os.path.isfile("Files/" + file+'.csv'):
        os.remove("Files/" + file+'.csv')
    df = pd.read_csv(file, delim_whitespace=True, header=None, encoding="windows-1250")
    df.to_csv(file+'.csv', index=False, header=["x","y"])
    if not os.path.isdir("Files"):
        os.mkdir("Files")
    shutil.move(file+'.csv', "Files/" + file+'.csv')
    return df
