import serial
import time
import struct
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())

for p in ports:
    if "Arduino" in p[1]:
        print("Arduino Port: "+str(p[0]))
        ser=serial.Serial(p[0], 9600, timeout=1)
        break

#ser.baudrate=9600
    
tempMeetingRoom = 0
humMeetingRoom = 0
tempLara = 0
tempExternal = 0

#data = 5.7
while True:
        try:
            ser.flush()
            read = ser.readline() 
            print(read)
            #ser.write(str(data))
            time.sleep(1)
            
            read = read[:-2]
                
            data = read.split("|")
            print(data)
            
            for values in data:
                print("Values: "+ str(values))
                try:
                    key,value = values.split(":")
                except:
                    key,value = "Not found", "Not found"
                
                print("key: "+ str(key))
                print("value: "+ str(value))
                
                if(key == 'TM'):
                    #print("Meeting Room")
                    tempMeetingRoom = value
                elif(key == 'HM'):
                    #print("Hum Meeting Room")
                    humMeetingRoom = value
                elif(key == 'TL'):
                    #print("Lara")
                    tempLara = value
                elif(key == 'TE'):
                    #print("External")
                    tempExternal = value
                
            print("Temperatura Sala de Reuniao: " + str(tempMeetingRoom))
            print("Humidade Sala de Reuniao: " + str(humMeetingRoom))
            print("Temperatura Lara: " + str(tempLara))
            print("Temperatura Externa: " + str(tempExternal))
            
        except:
            print("Sem dados")
            break
        #ser.flush()
##        ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
##        ser.baudrate=9600
        #data = data*2
        
# ser.write(bytes(x,'utf-8'))

# read = ser.readline() 
# print(read)