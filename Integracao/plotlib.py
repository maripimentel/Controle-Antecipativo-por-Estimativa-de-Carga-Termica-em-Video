# coding=utf-8
import matplotlib.pyplot as plt
import matplotlib
from sqlitelib import *
import math
import numpy as np

# coding=utf-8

def plotModel (database, name, controllerType):
    if(controllerType != 0):
        data = ReadTable(database)
    elif(controllerType == 0):
        data = ReadTableIdent(database)
        
    name = name.replace(" ","_")
    name = name.replace(":","-")
    
    TEMP = 23
    TEMP_EMPTY_ROOM = 30
    
    if(name == '2018-11-23_09-51-38_05'):
        energyTime = ['09-40','10-20','10-52','11-14','11-43','13-22','13-46','14-16','14-36']
        energyValue = [9041.93,9041.25,9042.61,9042.85,9043.26,9044.82,9045.35,9046.03,9046.46]
    else:
        energyTime = []
        energyValue = []
    
    energyHour = []
    energyMin = []
    for t in energyTime:
        t = t.split('-')
        energyHour.append(t[0])
        energyMin.append(t[1])
        
    if(controllerType == 0):
        title = 'Identificação do Modelo'.decode('utf-8')
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
    tempExternalAnterior = 0.0
    contArray = []
    numPeople = []
    numPeopleReal = []
    nPeopleReal = 2
    doorSignal = []
    
    inferior = []
    superior = []
    
    contEnergy = 0
    
    energy = []
    
    for line in data:
        
        time = line[0].decode("utf-8")
        
        time = time.replace(" ","_")
        time = time.replace(":","-")
    
        time = time.split("_")
        time = time[1]
        timeAux = time.split("-")
        hour = timeAux[0]
        min = timeAux[1]
        
        if(len(energyHour)>contEnergy+1):
            if(int(hour)>eneryHour[contEnergy+1] and int(min)>energyMin[contEnergy+1]):
                contEnergy = contEnergy+1
        if(len(energyHour)>0):
            energy.append(energyValue[contEnergy])
        
        dateTime.append(time)
        tempMeetingRoom.append(line[1])
        humMeetingRoom.append(line[2])
        
        if(math.isnan(float(line[3])) or line[3]=='nan' or int(line[3]) > 25):
            tempLara.append(tempLaraAnterior)
        else:
            tempLara.append(line[3])
            tempLaraAnterior = line[3]
            
        if(math.isnan(float(line[4])) or line[4]=='nan'):
            tempExternal.append(tempExternalAnterior)
        else:
            if(int(line[4]) < 100):
                tempExternal.append(line[4])
                tempExternalAnterior = line[4]
            else:
                tempExternal.append(25+((line[4]-30)/4))
        
        if(controllerType != 0):
            doorSignal.append(line[5])
            if(int(line[6])!=0 or controllerType!=3):
                reference.append(TEMP)
            else:
                reference.append(TEMP_EMPTY_ROOM)
            inferior.append(22.5)
            superior.append(23.5)
        #if(int(line[6]) < 6):
            
            if(int(hour) == 23 or int(hour) < 8):
                numPeople.append(0)
            else:
                if(line[6] < 0):
                    numPeople.append(0)
                elif(line[6] > 9):
                    numPeople.append(2)
                else:
                    numPeople.append(line[6])
            
        #else:
            #numPeople.append(6)
            compressorSignal.append(line[7])
            isOn.append(line[8])
            if(line[9] < 0):
                dutyCycle.append(0)
            else:
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
##        elif(hour=='10' and (min == '57' or min == '57')):
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
        else:
            compressorSignal.append(line[5])
            
        if(cont == 0 or cont % (57) == 0):
            dateTimeClean.append(str(int(hour))+":00")
            
            if(cont == 0):
                hourInitial = hour
            else:
                if(hour == hourInitial):
                    cont = cont + 1
                    break
                
##            if(int(hour) == 17):
##                cont = cont + 1
##                break
##                
        cont = cont+1
    
    N = 15*4
    cumsum, movingAves = [0], []
    
    tempMeetingRoomBig = []
    for i in range(N-1):
        tempMeetingRoomBig.append(tempMeetingRoom[1])
    for i in tempMeetingRoom:
        tempMeetingRoomBig.append(i)
    
    for i, x in enumerate(tempMeetingRoomBig, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            movingAve = (cumsum[i] - cumsum[i-N])/N
            movingAves.append(movingAve)
            
    
    integralE = 0
    integralL = 0
    integralNP = 0
    integralError = 0
    PMV = []
    PPD = []
    rmse = 0
    contOnTime = 0
    contOnTimeRef = 0
    wasOff = True
    rmsePermanente = 0
    contOnTimePermanente = 0
    if(controllerType != 0):
        for i in range(len(tempExternal)):
            tempE = tempExternal[i]
            isOnNow = isOn[i]
            tempL = tempLara[i]
            e = error[i]
            tempR = tempMeetingRoom[i]
            npeople = numPeople[i]
            
            integralNP = integralNP + npeople
            
            if(isOnNow):
                contOnTime = contOnTime + 1
                if(tempE > 23):
                    integralE = integralE + (tempE - 23)  
                    
                if(tempL > 23):
                    integralL = integralL + (tempL - 23)
                
                if(reference[i] == 23):
                    if(wasOff):
                        if(tempR < 23.5):
                            wasOff = False
                            contOnTimePermanente = contOnTimePermanente + 1
                            rmsePermanente = rmsePermanente + pow(e,2)
                    else:
                        contOnTimePermanente = contOnTimePermanente + 1
                        rmsePermanente = rmsePermanente + pow(e,2)
                    
                    contOnTimeRef = contOnTimeRef + 1
                    rmse = rmse + pow(e,2)
                    if(e > 0):
                        integralError = integralError + e
                    else:
                        integralError = integralError - e
                else:
                    wasOff = True
            else:
                wasOff = True
            
            if(tempR < 17):
                pmv = -1.77
            elif(tempR < 18):
                pmv = -1.5
            elif(tempR < 19):
                pmv = -1.27
            elif(tempR < 20):
                pmv = -1.02
            elif(tempR < 21):
                pmv = -0.77
            elif(tempR < 22):
                pmv = -0.5
            elif(tempR < 22.7):
                pmv = -0.25
            elif(tempR < 23.3):
                pmv = 0
            elif(tempR < 25):
                pmv = 0.27
            elif(tempR < 26):
                pmv = 0.5
            elif(tempR < 27):
                pmv = 0.78
            elif(tempR < 28):
                pmv = 1
            elif(tempR < 29):
                pmv = 1.29
            elif(tempR < 30):
                pmv = 1.6
            else:
                pmv = 1.8
                
##            if(reference[i] != 23):
##                pmv = 0
                
            PMV.append(pmv)
            
            ppd = 100 - 95 * np.exp(-0.03353*(pow(pmv,4))-0.2179*(pow(pmv,2)))
            
            PPD.append(ppd)
        
        N = 15
        pmvBig = []
        ppdBig = []
        for i in range(N-1):
            pmvBig.append(PMV[1])
            ppdBig.append(PPD[1])
        for i in PMV:
            pmvBig.append(i)
        for i in PPD:
            ppdBig.append(i)
    
    
        cumsum, PMVFilter = [0], []
        
        for i, x in enumerate(pmvBig, 1):
            cumsum.append(cumsum[i-1] + x)
            if i>=N:
                movingAve = (cumsum[i] - cumsum[i-N])/N
                PMVFilter.append(movingAve)
    
    
        N = 15
        cumsum, PPDFilter = [0], []
        
        for i, x in enumerate(ppdBig, 1):
            cumsum.append(cumsum[i-1] + x)
            if i>=N:
                movingAve = (cumsum[i] - cumsum[i-N])/N
                PPDFilter.append(movingAve)
    
    
    #matplotlib.rc('text', usetex=True)
    #matplotlib.rc('font', family='Arial')
    plt.figure()
    plt.plot(dateTime[1:], tempMeetingRoom[1:])
    plt.plot(dateTime[1:], movingAves[1:])
    if(controllerType != 0):
        plt.plot(dateTime[1:], reference[1:])
        plt.legend((r"$Temperatura\ da\ Sala\ de\ Reuni\~ao$", r"$M\'e dia\ M\'ovel\ da\ Temperatura$", r"$Refer\^encia$"), loc='upper right')
    else:
        plt.legend((r"$Temperatura\ da\ Sala\ de\ Reuni\~ao$", r"$M\'edia\ M\'ovel\ da\ Temperatura$"), loc='upper right')
    plt.title(title + " - Temperatura")
    plt.ylabel(r"$Temperatura\ (^o C)$")
    plt.xlabel(r"$Hor\'ario$")
    plt.xticks(range(0, cont,  (57)), dateTimeClean)
    plt.grid(True)
    plt.savefig("Log/"+save+"_"+name+"_Temp.png")
    plt.show()
    
    plt.figure()
    plt.plot(dateTime[1:], tempLara[1:])
    plt.plot(dateTime[1:], tempExternal[1:])
    plt.legend((r"$Temperatura\ da\ Sala\ Vizinha$", r"$Temperatura\ Externa$"), loc='upper left')
    plt.title(title + " - Perturbações de Temperaturas".decode("utf-8"))
    plt.ylabel(r"$Temperatura\ (^o C)$")
    plt.xlabel(r"$Hor\'ario$")
    plt.xticks(range(0, cont,  (57)), dateTimeClean)
    plt.grid(True)
    plt.savefig("Log/"+save+"_"+name+"_TempExt.png")
    plt.show()
    
    if(controllerType != 0):
        plt.figure()
        plt.plot(dateTime[1:], PMVFilter[1:])
        #plt.legend((r"$Sinal\ de\ Controle$", r"$Estado\ do\ Sistema$"), loc='lower left')
        plt.title(title + " - PMV")
        plt.ylabel(r"$PMV$")
        plt.xlabel(r"$Hor\'ario$")
        plt.xticks(range(0, cont,  (57)), dateTimeClean)
        plt.grid(True)
        plt.savefig("Log/"+save+"_"+name+"_PMV.png")
        plt.show()
        
        N = 1
        dutyCycleBig = []
        for i in range(N-1):
            if(dutyCycle[1] > 0):
                dutyCycleBig.append(dutyCycle[1])
            else:
                dutyCycleBig.append(0)
        for i in PMV:
            if(i>0):
                dutyCycleBig.append(i)
            else:
                dutyCycleBig.append(0)
    
    
        cumsum, dutyCycleFilter = [0], []
        
        for i, x in enumerate(dutyCycleBig, 1):
            cumsum.append(cumsum[i-1] + x)
            if i>=N:
                movingAve = (cumsum[i] - cumsum[i-N])/N
                dutyCycleFilter.append(movingAve)
    
        
        plt.figure()
        plt.plot(dateTime[1:], PPDFilter[1:])
        #plt.legend((r"$Sinal\ de\ Controle$", r"$Estado\ do\ Sistema$"), loc='lower left')
        plt.title(title + " - PPD")
        plt.ylabel(r"$PPD$")
        plt.xlabel(r"$Hor\'ario$")
        plt.xticks(range(0, cont,  (57)), dateTimeClean)
        plt.grid(True)
        plt.savefig("Log/"+save+"_"+name+"_PPD.png")
        plt.show()
        plt.figure()
        plotIsOn = False
        if(plotIsOn):
            plt.plot(dateTime[1:], isOn[1:])
        if(controllerType != 1):
            plt.plot(dateTime[1:], dutyCycle[1:], linewidth = 0.7)
        else:
            plt.plot(dateTime[1:], compressorSignal[1:], linewidth = 0.5)
        plt.title(title + " - Acionamento")
        if(controllerType != 1):
            if(plotIsOn):
                plt.legend((r"$Estado\ do\ Sistema$", r"$Ciclo\ de\ Trabalho$"), loc='upper left')
            #else:
               # plt.legend((r"$Ciclo\ de\ Trabalho$"), loc='upper left')
        else:
            plt.legend((r"$Estado\ do\ Sistema$", r"$Sinal\ de\ Controle$"), loc='lower left')
        plt.ylabel(r"$Sinal$")
        plt.xlabel(r"$Hor\'ario$")
        plt.xticks(range(0, cont,  (57)), dateTimeClean)
        plt.grid(True)
        plt.savefig("Log/"+save+"_"+name+"_Signal.png")
        plt.show()
        
        if(len(energy) > 0):
            plt.figure()
            plt.plot(dateTime[1:], energy[1:])
            plt.title(title + " - Consumo")
            plt.ylabel(r"$Consumo (KWh)$")
            plt.xlabel(r"$Hor\'ario$")
            plt.xticks(range(0, cont,  (57)), dateTimeClean)
            plt.grid(True)
            plt.savefig("Log/"+save+"_"+name+"_Energy.png")
            plt.show()
        
        plt.figure()
        plt.plot(dateTime[1:], numPeople[1:])
        plt.title(title + " - Contagem de Pessoas")
        plt.ylabel(r"$N\'umero\ de\ Pessoas$")
        plt.xlabel(r"$Hor\'ario$")
        plt.xticks(range(0, cont,  (57)), dateTimeClean)
        plt.grid(True)
        plt.savefig("Log/"+save+"_"+name+"_People.png")
        plt.show()
        
        plt.figure()
        plt.plot(dateTime[1:], doorSignal[1:])
        plt.title(title + " - Sinal da Porta")
        plt.ylabel(r"$Sinal$")
        plt.xlabel(r"$Hor\'ario$")
        plt.xticks(range(0, cont,  (57)), dateTimeClean)
        plt.grid(True)
        plt.savefig("Log/"+save+"_"+name+"_Door.png")
        plt.show()
    
    else:
        plt.figure()
        plt.plot(dateTime[1:], compressorSignal[1:])
        plt.title(title + " - Acionamento")
        plt.ylabel(r"$Sinal$")
        plt.xlabel(r"$Hor\'ario$")
        plt.xticks(range(0, cont,  (57)), dateTimeClean)
        plt.grid(True)
        plt.savefig("Log/"+save+"_"+name+"_Signal.png")
        plt.show()
        
    mediaExternal = sum(tempExternal)/float(len(tempExternal))
    mediaLara = sum(tempLara)/float(len(tempLara))
    mediaNP = sum(numPeople)/float(len(numPeople))
    
    
    
    print("\n\n---------------------------------")
    print("-------Analise de Dados----------")
    print("---------------------------------")
    
    print("\n------ Temperatura Externa ------")
    print("Media: " + str(mediaExternal))
    print("Integral: " + str(integralE))
    
    print("\n-- Temperatura da Sala Vizinha --")
    print("Media: " + str(mediaLara))
    print("Integral: " + str(integralL))
    
    print("\n------- Numero de Pessoas -------")
    print("Media: " + str(mediaNP))
    print("Integral: " + str(integralNP))
    
    rmseF = pow((rmse/float(contOnTime)),0.5)
    rmseC = pow((rmse/float(contOnTimeRef)),0.5)
    rmsePermanente = pow((rmsePermanente/float(contOnTimePermanente)),0.5)
    
    print("\n-------- Conforto Termico -------")
    print("Integral do erro: " + str(integralError))
    print("RMSE F: "+str(rmseF))
    print("RMSE C: "+str(rmseC))
    print("RMSE P: "+str(rmsePermanente))
    
        