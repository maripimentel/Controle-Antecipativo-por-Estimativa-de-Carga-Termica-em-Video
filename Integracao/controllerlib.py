import serial
import time
import struct
import serial.tools.list_ports

def Controller():
    TAG = '(controller) '
    
    output = 100
    
    (onTime, period) = PWM(output, TAG)
    
    writeRele(onTime, period, TAG)
    
def PWM(output, TAG):
    OUTPUT_MAX = 100
    PERIOD = 4 * 60
    
    period = float(PERIOD)
    
    percentage = float(output)/float(OUTPUT_MAX)
    
    if percentage > 0.9:
        percentage = 1
    elif percentage < 0:
        percentage = 0
    elif percentage < 0.1:
        percentage = 0.1
    
    onTime = period * percentage
    
    print(TAG+'Period: '+str(period))
    print(TAG+'Tempo Ligado: '+str(onTime))
    
    return (onTime, period)

def writeRele(onTime, period, TAG):
    
    ports = list(serial.tools.list_ports.comports())

    for p in ports:
        if "Arduino" in p[1]:
            print(TAG+"Arduino Port: "+str(p[0]))
            ser=serial.Serial(p[0], 9600, timeout=1)
    
    if (onTime>0):
        data = 'l'
        print(TAG + 'Sinal para o compressor ligar por '+str(onTime)+' segundos')
        ser.write(str(data))
        time.sleep(1)
        ser.flush()
        time.sleep(onTime)
        
    if (onTime != period):
        data = 'd'
        print(TAG + 'Sinal para o compressor desligar por '+str(period - onTime)+' segundos')
        ser.write(str(data))
        time.sleep(1)
        ser.flush()
        time.sleep(period - onTime)
        
