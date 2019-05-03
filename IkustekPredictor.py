from dataManager.RainDataManager import RainDataManager
from dataManager.TempDataManager import TempDataManager
from dataManager.BikeDataManager import BikeDataManager
from datetime import datetime, timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

futureStepsNum = 7

futureTemp = []

rainDM = RainDataManager()
tempDM = TempDataManager()
bikeDM = BikeDataManager()

'''
'''
rainDM.downloadDataMin()
tempDM.downloadDataMin()
bikeDM.downloadDataMin()

rainDM.workData()
tempDM.workData()
bikeDM.workData()

'''
rainDM.downloadData()
tempDM.downloadData()
bikeDM.downloadData()




tempDM.loadData()


start_date = date(2015, 1, 1)
end_date = datetime.now().date()
for single_date in daterange(start_date, end_date):
    print (tempDM.getDayValue(single_date))


for i in range(0, futureStepsNum):
    promptStr = "Please enter temp for day +" + str(i) + ": "
    temp = float(input(promptStr))
    print("You entered: " + str(temp))
    futureTemp.append(temp)

print(futureTemp)
'''
