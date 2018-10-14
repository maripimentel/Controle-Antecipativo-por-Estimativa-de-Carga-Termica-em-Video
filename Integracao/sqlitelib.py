##Controle Antecipativo por Estimativa de Carga Termica em Video
##Biblioteca para Comunicacao com a Base de Dados
##Trabalho de Graduacao
##Versao 1
##Autores:
##    Alexandre Saran
##    Mariana Pimentel

# coding=utf-8

import sqlite3
import serial.tools.list_ports
import time

# Inicialize database
def InicializeDatabase(name):
	database = sqlite3.connect('../../Dados/'+name)
	return database


# Create table "informacaoSala"
def CreateTable(database):
	cursor = database.cursor()
	cursor.execute('''
	    CREATE TABLE IF NOT EXISTS informacaoSala(dataHora TEXT PRIMARY KEY, tempSala REAL,
	                       humSala REAL, tempVizinha REAL, tempExterna REAL,
	                       sinalPorta INTEGER, numPessoas INTEGER, sinalCompressor INTEGER)
	''')
	database.commit()
	return database 

# Insert data in table
def InsertData(database, dateTime, tempMeetingRoom, humMeetingRoom, tempLara, tempExternal, doorSignal, numPeople, compressorSignal):
	cursor = database.cursor()
	TAG = '(sqlite) '
	try:
		cursor.execute('''INSERT INTO informacaoSala(dataHora,tempSala,humSala,tempVizinha,tempExterna,sinalPorta,numPessoas,sinalCompressor)
	                  VALUES(?,?,?,?,?,?,?,?)''', (dateTime, tempMeetingRoom, humMeetingRoom, tempLara, tempExternal, doorSignal, numPeople, compressorSignal))
		print(TAG+'dataHora:{0} | numPessoas:{1}'.format(dateTime, numPeople))
	except Exception as e:
		print(TAG+'Falha ao inserir dados')
	database.commit()
	return database

# Read all data from the table
def ReadTable(database):
	TAG = '(sqlite) '
	cursor = database.cursor()
	try:
		cursor.execute('''SELECT dataHora,tempSala,humSala,tempVizinha,tempExterna,sinalPorta,numPessoas,sinalCompressor FROM informacaoSala''')
	except Exception as e:
		print(TAG+'Falha ao ler os dados')
	# Prints each line information
	data = cursor.fetchall()
	cont = 0
	for line in data:
	    print(TAG+'Coluna[{0}] -> dataHora:{1} | tempSala:{2} | humSala:{3} | tempVizinha:{4} | tempExterna:{5} | sinalPorta:{6} | numPessoas:{7} | sinalCompressor:{8}'.format(cont, line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))
	    cont = cont + 1
	return data

# Close the table
def CloseTable(database):
	database.close()
	
def readTempHum(tempMeetingRoom, humMeetingRoom, tempLara, tempExternal):
    TAG = '(sqlite) '
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "Arduino" in p[1]:
                print(TAG+"Arduino Port: "+str(p[0]))
                ser=serial.Serial(p[0], 9600, timeout=1)
                break
    try:
        ser.flush()
        read = ser.readline()
        print(TAG + "read: " + str(read))
    except:
        print(TAG + "Sem dados")
        readOk = False
        return (readOk, tempMeetingRoom, humMeetingRoom, tempLara, tempExternal)
    
    if(read == "" or len(read) < 4):
        readOk = False
        return (readOk, tempMeetingRoom, humMeetingRoom, tempLara, tempExternal)
    time.sleep(1)
    read = read.decode("utf-8")
    #print(read)
    read = read[:-2]
    #print(read)
    data = read.split("|")
    print(TAG + "Data: " + str(data))
    
    for values in data:
        print(TAG + "Values: " + str(values))
        try:
            key,value = values.split(":")
        except:
            key,value = "Not found", "Not found"
            
        #print(key)
        #print(value)
        
        if(key == 'TM' and value != "Not found"):
        #    print("Temp Meeting Room")
            tempMeetingRoom = value[:]
        elif(key == 'HM' and value != "Not found"):
        #    print("Hum Meeting Room")
            humMeetingRoom = value
        elif(key == 'TL' and value != "Not found"):
        #    print("Lara")
            tempLara = value
        elif(key == 'TE' and value != "Not found"):
        #    print("External")
            tempExternal = value
            
    print(TAG + "Temperatura Sala de Reuniao: " + str(tempMeetingRoom))
    print(TAG + "Humidade Sala de Reuniao: " + str(humMeetingRoom))
    print(TAG + "Temperatura Lara: " + str(tempLara))
    print(TAG + "Temperatura Externa: " + str(tempExternal))
    readOk = True
            
    return (readOk, tempMeetingRoom, humMeetingRoom, tempLara, tempExternal)

