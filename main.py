from idlelib.iomenu import encoding
from urllib.request import urlopen

link = "https://physionet.org/physiobank/database/emgdb/RECORDS"

f = urlopen(link)
my_file = f.read()

new = str(my_file, encoding)
new = new.split()
file_Url = []

for x in new:
    file_Url.append("https://physionet.org/physiobank/database/emgdb/{0}{1}".format(x, ".txt"))

data = []
for x in file_Url:
    fe = urlopen(x)
    bytes_to_str = fe.read()
    #bytes_to_str = str(fe.read(), encoding)
    bytes_to_str = bytes_to_str.split()
    data.append(bytes_to_str)
print(data)
