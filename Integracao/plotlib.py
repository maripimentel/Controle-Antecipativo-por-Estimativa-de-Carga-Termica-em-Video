import matplotlib.pyplot as plt
from sqlitelib import *
import math

# coding=utf-8

def plotModel (database, name):
    data = ReadTable(database)
    
    TEMP = 21
    
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
        compressorSignal.append(line[7]*14)
        isOn.append(line[8])
        dutyCycle.append(line[9])
        error.append(line[1]-TEMP)
        contArray.append(cont)
        if(cont == 0 or cont%400 == 0):
            dateTimeClean.append(time)
        cont = cont+1
                
##        if(cont>1180):
##            break
    
    plt.figure()
    plt.plot(dateTime[1:], reference[1:])
    plt.plot(dateTime[1:], tempMeetingRoom[1:])
    plt.plot(dateTime[1:], tempLara[1:])
    plt.plot(dateTime[1:], tempExternal[1:])
    plt.plot(dateTime[1:], compressorSignal[1:])
    plt.plot(dateTime[1:], isOn[1:])
    plt.plot(dateTime[1:], error[1:])
    plt.plot(dateTime[1:], dutyCycle[1:])
    plt.legend(("Referencia","Temperatura da Sala de Reuniao", "Temperatura do Lara", "Temperatura Externa", "Sinal de Controle", "Estado do Sistema", "Erro", "Ciclo de Trabalho"), loc='lower left')
    plt.title("Controlador PI")
    plt.ylabel("Temperatura")
    plt.xlabel("Horario")
    plt.xticks(range(0, 1500, 400), dateTimeClean)
    plt.grid(True)
    plt.savefig("Log/PI_"+name+".png")
    plt.show()
    name = name.replace(" ","|")
    print(name)
    
    print(tempMeetingRoom[360])
    print(dutyCycle[360])
        