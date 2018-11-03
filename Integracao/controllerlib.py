import serial
import time
import struct
import serial.tools.list_ports
import settings
from scipy import signal
from simple_pid import PID

def Controller(lastOutput, cont):
    TAG = '(controller) '

    if (settings.controllerType == 0):
        # Identificacao do Modelo

        print(TAG + "Identificacao do Modelo")

        PERIOD = 60 # 4 horas
        
        print(TAG + "Contador: " + str(cont))
        
        if (cont >= 3 * 60):
            settings.isOn = 0
            output = 0
            if (cont == 4 * 60):
                cont = 1
            else:
                cont = cont + 1
        else:
            settings.isOn = 1
            output = 100
            cont = cont + 1 
        
        
    elif(settings.controllerType == 1):
        # Liga-Desliga

        print(TAG + "Controlador: Liga-Desliga")

        PERIOD = 10 # 10 segundos

        MIN_TEMP = 20
        MAX_TEMP = 22

        print(TAG + "Contador: " + str(cont))
        print(TAG + "Temperatuda da Sala: "+ str(settings.tempMeetingRoom))
        
        if (cont >= 3 * 60 * 6):
            settings.isOn = 0
            output = 0
            if (cont == 4 * 60 * 6):
                cont = 1
            else:
                cont = cont + 1
        else:
            settings.isOn = 1
            if(float(settings.tempMeetingRoom) > 22.00):
                print(TAG + "Liga-Desliga: LIGA")
                output = 100
            elif(float(settings.tempMeetingRoom) < 20.00):
                print(TAG + "Liga-Desliga: DESLIGA")
                output = 0
            else:
                print(TAG + "Liga-Desliga: MANTEM")
                output = lastOutput
            cont = cont + 1

    elif(settings.controllerType == 2):
        # PI
        print(TAG + "Controlador: PI")

        PERIOD = 60 * 4

        TEMP = 23.0

        Kp = 0.12
        Ki = 13 * Kp;
        
        if(cont > 3 * 15):        
            settings.isOn = 0
            output = 0
            if (cont == 4 * 15):
                cont = 1
            else:
                cont = cont + 1
        else:
            settings.isOn = 1
            
            cont = cont + 1
            
            # PI
            piController = PID (-Kp, -Ki, 0, setpoint = TEMP)
            
            # Erro: diferenca entre temperatura desejada e medida
            error = float(settings.tempMeetingRoom) - TEMP
            
            # Sinal de controle
            controllerSignal = piController(float(settings.tempMeetingRoom))
            print(TAG + "Controller Signal: " + str(controllerSignal))

            # Saturacao
            if (controllerSignal>0.3):
                    controllerSignal = 0.3;
            elif (controllerSignal < 0):
                    controllerSignal = 0;

            output = controllerSignal * 100.0 / 0.3;
            
            print(TAG + "Controller Signal: " + str(output))
        
##    elif(settings.controllerType == 3):
##        #Adaptativo
    
    (onTime, period) = PWM(output, PERIOD, TAG)
    
    writeRele(onTime, period, TAG)

    return (output, cont)

    
def PWM(output, PERIOD, TAG):
    OUTPUT_MAX = 100
    
    period = float(PERIOD)
    
    percentage = float(output)/float(OUTPUT_MAX)
    
    if percentage > 0.9:
        percentage = 1
    elif percentage <= 0:
        percentage = 0
    elif percentage < 0.1:
        percentage = 0.1
    
    settings.dutyCycle = percentage
    
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
        settings.compressorSignal = 1
        data = b"1"
        print(TAG + 'Sinal para o compressor ligar por '+str(onTime)+' segundos')
        ser.write(data)
        time.sleep(1)
        ser.flush()
        time.sleep(onTime)
        
    if (onTime != period):
        settings.compressorSignal = 0
        data = b"0"
        print(TAG + 'Sinal para o compressor desligar por '+str(period - onTime)+' segundos')
        ser.write(data)
        time.sleep(1)
        ser.flush()
        time.sleep(period - onTime)
        
