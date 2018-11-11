
def init():
    global cntUp
    global cntDown
    global camera
    global controllerType
    global tempMeetingRoom
    global dutyCycle
    global isOn
    global inicialNumPeople

    cntUp = 0
    cntDown = 0
    tempMeetingRoom = 0
    compressorSignal = 0
    dutyCycle = 0
    isOn = 0
    inicialNumPeople = 4

    # Tipos de Controladores
    # 0 -> Identificacao do Modelo
    # 1 -> Liga-Desliga
    # 2 -> PI
    # 3 -> Antecipativo
    controllerType = 3