import pandas as pd
import os
import shutil


def parse_to_csv(data):
    df = []
    filenames = []
    for x in data:
        open(str(x)+'.txt', 'wb').write(data[x].read())
        df.append(parse_to_csv_local(str(x)+'.txt'))
    for x in data:
        filenames.append(str(x) + '.txt.csv')
        os.remove(str(x)+'.txt')
    return [df, filenames]


def parse_to_csv_local(file):
    if os.path.isfile("Files/" + file+'.csv'):
        os.remove("Files/" + file+'.csv')
    df = pd.read_csv(file, delim_whitespace=True, header=None, encoding="windows-1250")
    df1 = pd.to_numeric(df[1], errors='coerce')
    df[1] = df1
    df.to_csv(file+'.csv', index=False, header=["x","y"])
    print(df.dtypes)
    if not os.path.isdir("Files"):
        os.mkdir("Files")
    shutil.move(file+'.csv', "Files/" + file+'.csv')
    return df
