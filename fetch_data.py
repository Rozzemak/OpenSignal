from idlelib.iomenu import encoding
from urllib.request import urlopen


class FetchData:
    def __init__(self, link):
        self.link = link

    #"https://physionet.org/physiobank/database/emgdb/RECORDS"
    def get_urls(self):
        new = self.get_file_name()
        file_url = []
        for x in new:
            file_url.append("https://physionet.org/physiobank/database/emgdb/{0}{1}".format(x, ".txt"))
        return file_url

    def get_file_name(self):
        f = urlopen(self.link)
        my_file = f.read()
        new = str(my_file, encoding)
        new = new.split()
        return new

    def get_data(self):
        data = self.get_urls()
        name = self.get_file_name()
        http_response = {}
        i = 0
        for x in data:
            fe = urlopen(x)
            http_response[name[i]] = fe
            i += 1
        return http_response





