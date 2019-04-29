import urllib.request
import os
import errno
import json
from dataManager.DataManager import DataManager


class RainDataManager(DataManager):

    def __init__(self):
        self.urlBase = 'http://kocher.es/meteotemplate/pages/station/climateRGraphMonthAjax.php?month='
        self.targetDataFile = 'data/rain/rain_by_day.json'

    def downloadData(self):
        for j in range(1, 13):
            filename ='data/rain/' + str(j).zfill(2) + "_rain.json"
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            urlStr = self.urlBase + str(j)
            with open(filename, "a") as myfile:
                with urllib.request.urlopen(urlStr) as url:
                    # data = json.loads(url.read().decode())
                    myfile.write(url.read().decode('utf-8'))

    def workData(self):
        yearsDict = {}
        for year in range(2015, 2020):
            monthsDict = {}
            for month in range(1, 13):
                monthsDict[str(month)] = {}
            yearsDict[str(year)] = monthsDict

        for month in range(1, 13):
            with open('data/rain/' + str(month).zfill(2) + '_rain.json') as json_file:
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
            myfile.write(json.dumps(yearsDict))
