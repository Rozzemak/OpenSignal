from idlelib.iomenu import encoding
from urllib.request import urlopen


class FetchData:
    def __init__(self, link):
        self.link = link

    #"https://physionet.org/physiobank/database/emgdb/RECORDS"
    def get_urls(self):
        f = urlopen(self.link)
        my_file = f.read()
        new = str(my_file, encoding)
        new = new.split()
        file_url = []

        for x in new:
            file_url.append("https://physionet.org/physiobank/database/emgdb/{0}{1}".format(x, ".txt"))
        print(file_url)
        return file_url

    def get_data(self):
        data = self.get_urls()
        http_response = []
        for x in data:
            fe = urlopen(x)
            http_response.append(fe)
        return http_response





