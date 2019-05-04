from Parser import Parser as Pr
from fetch_data import FetchData
from bokeh.plotting import figure, output_file, show
import pandas as pd
from bokeh.models import DatetimeTickFormatter, ColumnDataSource

fetch_data = FetchData("https://physionet.org/physiobank/database/emgdb/RECORDS")
l = fetch_data.get_data()
dfs = Pr.parse_to_csv(l)

healthy = pd.read_csv("Files/emg_healthy.txt.csv")
myopathy = pd.read_csv("Files/emg_myopathy.txt.csv")
neuropathy = pd.read_csv("Files/emg_neuropathy.txt.csv")

#source = ColumnDataSource(dfs[0])

#Take data  and present in a graph
output_file("test.html")
p = figure(plot_width=1280, plot_height=720)
p.line(x='x',y='y',line_width=1, source=neuropathy)

show(p)
