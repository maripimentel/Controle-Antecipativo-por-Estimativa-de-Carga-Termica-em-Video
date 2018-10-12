import serial
import time
import struct

ser=serial.Serial("/dev/ttyACM0",9600,timeout=1)  #change ACM number as found from ls /dev/tty/ACM*
#ser.baudrate=9600

#data = 5.7
while True:
        try:
            ser.flush()
            read = ser.readline() 
            print(read)
            #ser.write(str(data))
            time.sleep(1)
        except:
            print("Sem dados")
        #ser.flush()
##        ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
##        ser.baudrate=9600
        #data = data*2
        
# ser.write(bytes(x,'utf-8'))

# read = ser.readline() 
# print(read)