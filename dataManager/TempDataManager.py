import urllib.request
import os
import errno
import json
from datetime import datetime

from dataManager.DataManager import DataManager


class TempDataManager(DataManager):

    def __init__(self):
        self.urlBase = 'http://kocher.es/meteotemplate/pages/station/climateTGraphMonthAjax.php?q=avg&month='
        self.targetDataFile = 'data/temperature/temp_by_day.json'

    def downloadDataMin(self, curMonth=None):
        month = datetime.today().month
        if(curMonth is not None):
            month = curMonth

        filename ='data/temperature/' + str(month).zfill(2) + "_temp.json"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        urlStr = self.urlBase + str(month)
        with open(filename, "w") as myfile:
            myfile.truncate()
            with urllib.request.urlopen(urlStr) as url:
                # data = json.loads(url.read().decode())
                myfile.write(url.read().decode('utf-8'))


    def downloadData(self):
        for j in range(1, 13):
            self.downloadDataMin(curMonth=j)

    def workData(self):
        yearsDict = {}
        for year in range(2015, 2020):
            monthsDict = {}
            for month in range(1, 13):
                monthsDict[str(month)] = {}
            yearsDict[str(year)] = monthsDict

        for month in range(1, 13):
            with open('data/temperature/' + str(month).zfill(2) + '_temp.json') as json_file:
                data = json.load(json_file)
                data = data['data']
                print(len(data))
                for yearData in range(len(data)):
                    year = data[yearData]['name']
                    if year >= 2015:
                        print(data[yearData]['name'])
                        for idx, dayTemp in enumerate(data[yearData]['data'], start=1):
                            print(str(idx) + '-->' + str(dayTemp))
                            yearsDict[str(year)][str(month)][str(idx)] = dayTemp

        print(yearsDict)

        with open(self.targetDataFile, "a") as myfile:
            myfile.truncate()
            myfile.write(json.dumps(yearsDict))
