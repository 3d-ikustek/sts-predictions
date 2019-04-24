import urllib.request
import os
import errno
import json
from datetime import date


class DataManager:

    def __init__(self):
        self.urlBase = ''
        self.targetDataFile = ''
        self.data = ''

    def loadData(self):
        print(self.urlBase)
        with open(self.targetDataFile) as json_file:
            self.data = json.load(json_file)

    def getDayValue(self, oneDate):
        return self.data[str(oneDate.year)][str(oneDate.month)][str(oneDate.day)]
