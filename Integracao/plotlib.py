import matplotlib.pyplot as plt
from sqlitelib import *

# coding=utf-8

def plotModel (database, name):
    data = ReadTable(database)
    
    dateTime = []
    tempMeetingRoom = []
    humMeetingRoom = []
    tempLara = []
    tempExternal = []
    cont = 1
    contArray = []
    
    for line in data:
        dateTime.append(line[0])
        tempMeetingRoom.append(line[1])
        humMeetingRoom.append(line[2])
        tempLara.append(line[3])
        tempExternal.append(line[4])
        contArray.append(cont)
        cont = cont+1
    
    plt.figure()
    plt.plot(contArray, tempMeetingRoom)
    plt.title("Identificação do Modelo")
    plt.ylabel("Temperatura")
    plt.xlabel("Minutos")
    #plt.xticks(range(0, 80, 20), dateTime)
    plt.grid(True)
    plt.savefig("Log/IdentModelo_"+name+".png")
    plt.show()
    name = name.replace(" ","|")
    print(name)
        