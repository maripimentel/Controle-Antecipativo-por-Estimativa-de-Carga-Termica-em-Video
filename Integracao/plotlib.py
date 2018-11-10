import matplotlib.pyplot as plt
from sqlitelib import *
import math

# coding=utf-8

def plotModel (database, name, controllerType):
    data = ReadTable(database)
    
    name = name.replace(" ","_")
    name = name.replace(":","-")
    
    TEMP = 23
    
    if(controllerType == 0):
        title = 'Identificacao do Modelo'
        save = 'Ident'
    elif(controllerType == 1):
        title = 'Controlador Liga-Desliga'
        save = 'Liga-Deliga'
    elif(controllerType == 2):
        title = 'Controlador PI'
        save = 'PI'
    elif(controllerType == 3):
        title = 'Controlador Antecipativo'
        save = 'Antecipativo'
    
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
    numPeople = []
    numPeopleReal = []
    nPeopleReal = 2
    
    inferior = []
    superior = []
    
    for line in data:
        
        time = line[0].decode("utf-8")
        time = time.split(" ")
        time = time[1]
        timeAux = time.split(":")
        hour = timeAux[0]
        min = timeAux[1]
        
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
        numPeople.append(line[6])
        compressorSignal.append(line[7])
        isOn.append(line[8])
        dutyCycle.append(line[9])
        error.append(line[1]-TEMP)
        contArray.append(cont)
##        
##        if(hour=='10' and (min == '10' or min == '11')):
##            nPeopleReal = 3
##        elif(hour=='10' and (min == '28' or min == '29')):
##            nPeopleReal = 4
##        elif(hour=='10' and (min == '44' or min == '45')):
##            nPeopleReal = 3
##        elif(hour=='10' and (min == '46' or min == '47')):
##            nPeopleReal = 4
##        elif(hour=='10' and (min == '51' or min == '52')):
##            nPeopleReal = 2
##        elif(hour=='10' and (min == '55' or min == '56')):
##            nPeopleReal = 4
##        elif(hour=='11' and (min == '04' or min == '05')):
##            nPeopleReal = 5
##        elif(hour=='11' and (min == '34' or min == '35')):
##            nPeopleReal = 6
##        elif(hour=='11' and (min == '45' or min == '46')):
##            nPeopleReal = 5
##        elif(hour=='12' and (min == '00' or min == '01')):
##            nPeopleReal = 4
##        elif(hour=='12' and (min == '11' or min == '12')):
##            nPeopleReal = 3
##        elif(hour=='12' and (min == '20' or min == '21')):
##            nPeopleReal = 2
##        elif(hour=='12' and (min == '27' or min == '28')):
##            nPeopleReal = 3
##        elif(hour=='12' and (min == '42' or min == '43')):
##            nPeopleReal = 4
##        elif(hour=='12' and (min == '49' or min == '50')):
##            nPeopleReal = 3
##        elif(hour=='12' and (min == '51' or min == '52')):
##            nPeopleReal = 1
##        elif(hour=='13' and (min == '30' or min == '31')):
##            nPeopleReal = 4
##        elif(hour=='13' and (min == '51' or min == '52')):
##            nPeopleReal = 5
##        elif(hour=='13' and (min == '53' or min == '54')):
##            nPeopleReal = 6
##        elif(hour=='14' and (min == '25' or min == '26')):
##            nPeopleReal = 5
##        elif(hour=='15' and (min == '08' or min == '09')):
##            nPeopleReal = 6
##        elif(hour=='16' and (min == '06' or min == '07')):
##            nPeopleReal = 7
##        elif(hour=='16' and (min == '15' or min == '16')):
##            nPeopleReal = 6
##        elif(hour=='16' and (min == '27' or min == '28')):
##            nPeopleReal = 5
##        elif(hour=='16' and (min == '40' or min == '41')):
##            nPeopleReal = 3
##        elif(hour=='16' and (min == '52' or min == '53')):
##            nPeopleReal = 4
##        elif(hour=='17' and (min == '00' or min == '01')):
##            nPeopleReal = 5
##        elif(hour=='17' and (min == '20' or min == '21')):
##            nPeopleReal = 3
##        elif(hour=='17' and (min == '30' or min == '31')):
##            nPeopleReal = 2
##        elif(hour=='17' and (min == '51' or min == '52')):
##            nPeopleReal = 0
            
##        numPeopleReal.append(nPeopleReal)
        
        if(cont == 0 or cont%170 == 0):
            dateTimeClean.append(str(int(hour))+":00")
        cont = cont+1
    
    plt.figure()
    plt.plot(dateTime[1:], tempMeetingRoom[1:])
    plt.plot(dateTime[1:], tempLara[1:])
    plt.plot(dateTime[1:], tempExternal[1:])
    plt.plot(dateTime[1:], reference[1:])
    plt.legend(("Temperatura da Sala de Reuniao", "Temperatura do Lara", "Temperatura Externa", "Referencia"), loc='upper right')
    plt.title(title)
    plt.ylabel("Temperatura")
    plt.xlabel("Horario")
    plt.xticks(range(0, cont, 170), dateTimeClean)
    plt.grid(True)
    plt.savefig("Log/"+save+"_"+name+"_Temp.png")
    plt.show()
    
    if(controllerType != 0):
        plt.figure()
        plt.plot(dateTime[1:], compressorSignal[1:], linewidth=0.5)
        if(controllerType != 1):
            plt.plot(dateTime[1:], dutyCycle[1:])
        plt.plot(dateTime[1:], isOn[1:])
        #plt.plot(dateTime[1:], error[1:])
        #plt.plot(dateTime[1:], inferior[1:])
        #plt.plot(dateTime[1:], superior[1:])
        if(controllerType != 1):
            plt.legend(("Sinal de Controle", "Ciclo de Trabalho", "Estado do Sistema"), loc='lower left')
        else:
            plt.legend(("Sinal de Controle", "Estado do Sistema"), loc='lower left')
        plt.title(title)
        plt.ylabel("Sinal")
        plt.xlabel("Horario")
        plt.xticks(range(0, cont, 170), dateTimeClean)
        plt.grid(True)
        plt.savefig("Log/"+save+"_"+name+"_Signal.png")
        plt.show()
    
        plt.figure()
        plt.plot(dateTime[1:], numPeople[1:])
        #plt.plot(dateTime[1:], numPeopleReal[1:])
        plt.title(title)
        plt.ylabel("Numero de Pessoas")
        plt.xlabel("Horario")
        plt.xticks(range(0, cont, 170), dateTimeClean)
        plt.grid(True)
        plt.savefig("Log/"+save+"_"+name+"_People.png")
        plt.show()

    

        