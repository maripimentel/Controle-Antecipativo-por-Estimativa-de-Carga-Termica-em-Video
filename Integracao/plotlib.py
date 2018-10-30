import matplotlib.pyplot as plt
from sqlitelib import *

# coding=utf-8

def plotModel (database, name):
    data = ReadTable(database)
    
    dateTime = []
    dateTimeClean = []
    tempMeetingRoom = []
    humMeetingRoom = []
    tempLara = []
    tempExternal = []
    compressorSignal = []
    isOn = []
    cont = 0
    contArray = []
    
    for line in data:
        time = line[0].decode("utf-8")
        time = time.split(" ")
        time = time[1]
        dateTime.append(time)
        tempMeetingRoom.append(line[1])
        humMeetingRoom.append(line[2])
        tempLara.append(line[3])
        tempExternal.append(line[4])
        compressorSignal.append(line[7]*15)
        isOn.append(line[8])
        contArray.append(cont)
        if(cont == 0 or cont%100 == 0):
            dateTimeClean.append(time)
        cont = cont+1
                
##        if(cont>1180):
##            break
    
    plt.figure()
    plt.plot(dateTime[1:], tempMeetingRoom[1:])
    plt.plot(dateTime[1:], tempLara[1:])
    plt.plot(dateTime[1:], tempExternal[1:])
    plt.plot(dateTime[1:], compressorSignal[1:])
    plt.plot(dateTime[1:], isOn[1:])
    plt.legend(("Temperatura da Sala de Reuniao", "Temperatura do Lara", "Temperatura Externa", "Sinal de Controle", "Estado do Sistema"), loc='lower left')
    plt.title("Controlador PI")
    plt.ylabel("Temperatura")
    plt.xlabel("Horario")
    plt.xticks(range(0, 500, 100), dateTimeClean)
    plt.grid(True)
    plt.savefig("Log/PI_"+name+".png")
    plt.show()
    name = name.replace(" ","|")
    print(name)
        