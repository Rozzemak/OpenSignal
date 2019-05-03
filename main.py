from fetch_data import FetchData
from Parser import Parser as Pr

fetch_data = FetchData("https://physionet.org/physiobank/database/emgdb/RECORDS")
l = fetch_data.get_data()
Pr.parse_to_csv(l)

