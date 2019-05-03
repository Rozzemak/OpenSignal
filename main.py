from fetch_data import FetchData

fetch_data = FetchData("https://physionet.org/physiobank/database/emgdb/RECORDS")
l = fetch_data.get_data()
for x in l:
    print(x.read())
