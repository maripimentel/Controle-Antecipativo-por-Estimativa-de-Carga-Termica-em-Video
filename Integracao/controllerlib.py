import serial
import time
import struct

def Controller():
    TAG = '(controller) '
    
    output = 50
    
    (onTime, period) = PWM(output, TAG)
    
    writeRele(onTime, period, TAG)
    
def PWM(output, TAG):
    OUTPUT_MAX = 100
    PERIOD = 4 * 60
    
    period = float(PERIOD)
    
    percentage = float(output)/float(OUTPUT_MAX)
    
    if percentage>0.9:
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
    
    ser=serial.Seria("/dev/ttyACM0",14400, timeout=1)
    
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