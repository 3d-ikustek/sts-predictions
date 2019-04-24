from dataManager.RainDataManager import RainDataManager

futureStepsNum = 7

futureTemp = []

rainDM = RainDataManager()
# rainDM.workData()


for i in range(0, futureStepsNum):
    promptStr = "Please enter temp for day +" + str(i) + ": "
    temp = float(input(promptStr))
    print("You entered: " + str(temp))
    futureTemp.append(temp)

print(futureTemp)
