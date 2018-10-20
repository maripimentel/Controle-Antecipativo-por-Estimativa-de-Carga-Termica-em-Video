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
    compressorSignal = []
    cont = 0
    contArray = []
    
    for line in data:
        time = line[0].decode("utf-8")
        time = time.split(" ")
        time = time[1]
        dateTime.append(time)
        print(time)
        tempMeetingRoom.append(line[1])
        humMeetingRoom.append(line[2])
        tempLara.append(line[3])
        tempExternal.append(line[4])
        compressorSignal.append(line[7]*15)
        contArray.append(cont)
        cont = cont+1
        
##        if(cont>1180):
##            break
    
    plt.figure()
    plt.plot(dateTime, tempMeetingRoom)
    plt.plot(dateTime, tempLara)
    plt.plot(dateTime, tempExternal)
    plt.plot(dateTime, compressorSignal)
    plt.legend(("Temperatura da Sala de Reuniao", "Temperatura do Lara", "Temperatura Externa", "Sinal de Controle"))
    plt.title("Identificacao do Modelo")
    plt.ylabel("Temperatura")
    plt.xlabel("Minutos")
    #plt.xticks(range(0, 80, 20), dateTime)
    plt.grid(True)
    plt.savefig("Log/IdentModelo_"+name+".png")
    plt.show()
    name = name.replace(" ","|")
    print(name)
        