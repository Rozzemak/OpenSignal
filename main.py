from idlelib.iomenu import encoding
from urllib.request import urlopen
from fetch_data import FetchData

fetch_data = FetchData("https://physionet.org/physiobank/database/emgdb/RECORDS")
print(fetch_data.get_data())

