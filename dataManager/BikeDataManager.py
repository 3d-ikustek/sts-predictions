import urllib.request
import os
import errno
import json
from datetime import datetime

from dataManager.DataManager import DataManager


class BikeDataManager(DataManager):

    def __init__(self):
        self.hostUrl = 'https://www.donostia.eus'
        self.urlBase = '/info/ciudadano/Videowall.nsf/movimientos.xsp?'
        self.targetDataFile = 'data/bikes/bikes_count_by_day.json'

    def downloadDataMin(self, curYear=None, curMonth=None):
        year = datetime.today().year
        month = datetime.today().month
        if(curYear is not None):
            year = curYear
        if(curMonth is not None):
            month = curMonth

        filename ='data/bikes/' + str(year) + "/" + str(month).zfill(2) + "_bikes.json"

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        with open(filename, "w") as myfile:
            myfile.truncate()
            fechaDesde = str(year) + '-' + str(month) + '-01'
            fechaHasta = ''
            if month == 12:
                print(str(year) + '-' + str(month) + ' to ' + str(year+1) + '-' + str(1))
                fechaHasta = str(year+1) + '-' + str(1).zfill(2) + '-01'
            else:
                print(str(year) + '-' + str(month) + ' to ' + str(year) + '-' + str(month+1))
                fechaHasta = str(year) + '-' + str(month+1).zfill(2) + '-01'

            urlStr = self.hostUrl + self.urlBase
            urlStr = urlStr + 'fecha_inicial=' + fechaDesde
            urlStr = urlStr + '&fecha_final=' + fechaHasta
            print(urlStr)

            with urllib.request.urlopen(urlStr) as url:
                # data = json.loads(url.read().decode())
                myfile.write(url.read().decode('utf-8'))


    def downloadData(self):
        for i in range(2015, 2020):
            for j in range(1, 13):
               self.downloadDataMin(curYear=i, curMonth=None)

    def workData(self):
        today = datetime.today()
        yearsDict = {}
        for year in range(2015, 2020):
            print(str(year))
            monthsDict = {}
            for month in range(1, 13):
                print(str(month))

                with open('data/bikes/' + str(year) + '/' + str(month).zfill(2) + '_bikes.json') as json_file:
                    if year == today.year and month > today.month:
                        None
                    else:
                        data = json.load(json_file)
                        datePattern = '%Y-%m-%d %H:%M:%S'
                        daysCont = {}
                        for i in reversed(range(0, len(data))):
                            fechaDesengancheStr = data[i]['fecha_desenganche']
                            fechaDesenganche = datetime.strptime(fechaDesengancheStr, datePattern)

                            if str(fechaDesenganche.day) in daysCont.keys():
                                daysCont[str(fechaDesenganche.day)] = daysCont[str(fechaDesenganche.day)] + 1
                            else:
                                daysCont[str(fechaDesenganche.day)] = 1
                        monthsDict[str(month)] = daysCont

            yearsDict[str(year)] = monthsDict

        print(yearsDict)

        with open(self.targetDataFile, "w") as myfile:
            myfile.truncate()
            myfile.write(json.dumps(yearsDict))
