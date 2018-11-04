import matplotlib.pyplot as plt
from sqlitelib import *
import math

# coding=utf-8

def plotModel (database, name):
    data = ReadTable(database)
    
    TEMP = 23
    
    dateTime = []
    dateTimeClean = []
    tempMeetingRoom = []
    humMeetingRoom = []
    tempLara = []
    tempExternal = []
    reference = []
    compressorSignal = []
    dutyCycle = []
    isOn = []
    error = []
    cont = 0
    tempLaraAnterior = 0.0
    contArray = []
    
    inferior = []
    superior = []
    
    for line in data:
        time = line[0].decode("utf-8")
        time = time.split(" ")
        time = time[1]
        dateTime.append(time)
        tempMeetingRoom.append(line[1])
        humMeetingRoom.append(line[2])
        if(math.isnan(float(line[3])) or line[3]=='nan'):
            tempLara.append(tempLaraAnterior)
        else:
            tempLara.append(line[3])
            tempLaraAnterior = line[3]
        tempExternal.append(line[4])
        reference.append(TEMP)
        inferior.append(22.5)
        superior.append(23.5)
        compressorSignal.append(line[7])
        isOn.append(line[8])
        dutyCycle.append(line[9])
        error.append(line[1]-TEMP)
        contArray.append(cont)
        if(cont == 0 or cont%200 == 0):
            dateTimeClean.append(time)
        cont = cont+1
    
    plt.figure()
    plt.plot(dateTime[1:], tempMeetingRoom[1:])
    plt.plot(dateTime[1:], tempLara[1:])
    plt.plot(dateTime[1:], tempExternal[1:])
    plt.plot(dateTime[1:], reference[1:])
    plt.legend(("Temperatura da Sala de Reuniao", "Temperatura do Lara", "Temperatura Externa", "Referencia"), loc='upper left')
    plt.title("Controlador Liga-Desliga")
    plt.ylabel("Temperatura")
    plt.xlabel("Horario")
    plt.xticks(range(0, 1500, 200), dateTimeClean)
    plt.grid(True)
    plt.savefig("Log/LigaDesliga_"+name+"_Temp.png")
    plt.show()
    
    plt.figure()
    plt.plot(dateTime[1:], compressorSignal[1:], linewidth=0.5)
    plt.plot(dateTime[1:], dutyCycle[1:])
    plt.plot(dateTime[1:], isOn[1:])
    #plt.plot(dateTime[1:], error[1:])
    #plt.plot(dateTime[1:], inferior[1:])
    #plt.plot(dateTime[1:], superior[1:])
    plt.legend(("Sinal de Controle", "Ciclo de Trabalho", "Estado do Sistema"), loc='lower left')
    plt.title("Controlador Liga-Desliga")
    plt.ylabel("Sinal")
    plt.xlabel("Horario")
    plt.xticks(range(0, 1500, 200), dateTimeClean)
    plt.grid(True)
    plt.savefig("Log/LigaDesliga_"+name+"_Signal.png")
    plt.show()
    
    
    name = name.replace(" ","|")
    print(name)
    
    print(tempMeetingRoom[360])
    print(dutyCycle[360])
        