import pandas as pd
import os
import shutil
import requests


def parse_to_csv(data):
    i = 1
    for x in data:
        open('data'+str(i)+'.txt', 'wb').write(x.read())
        parse_to_csv_local('data'+str(i)+'.txt')
        i = i+1

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
