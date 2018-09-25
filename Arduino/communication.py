import serial
import time
import struct

ser=serial.Serial("/dev/ttyACM0",14400, timeout=1)  #change ACM number as found from ls /dev/tty/ACM*
#ser.baudrate=9600

data = 5.7
while True:
        ser.write(str(data))
        time.sleep(1)
        ser.flush()
##        ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
##        ser.baudrate=9600
        #data = data*2
        
# ser.write(bytes(x,'utf-8'))

# read = ser.readline() 
# print(read)