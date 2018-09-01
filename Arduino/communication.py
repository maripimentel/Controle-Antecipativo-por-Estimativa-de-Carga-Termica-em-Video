import serial

ser=serial.Serial("/dev/ttyACM0",9600)  #change ACM number as found from ls /dev/tty/ACM*
ser.baudrate=9600

ser.write(bytes('5','utf-8'))

read = ser.readline()
print(read)