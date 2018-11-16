
def init():
    global cntUp
    global cntDown
    global camera
    global controllerType
    global tempMeetingRoom
    global tempLara
    global tempExternal
    global dutyCycle
    global isOn
    global inicialNumPeople

    cntUp = 0
    cntDown = 0
    tempMeetingRoom = 0
    tempLara = 0
    tempExternal = 0
    compressorSignal = 0
    dutyCycle = 0
    isOn = 0
    inicialNumPeople = 3

    # Tipos de Controladores
    # 0 -> Identificacao do Modelo
    # 1 -> Liga-Desliga
    # 2 -> PI
    # 3 -> Antecipativo
    controllerType = 3