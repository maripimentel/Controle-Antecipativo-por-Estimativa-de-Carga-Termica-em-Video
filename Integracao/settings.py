
def init():
    global cntUp
    global cntDown
    global camera
    global controllerType
    global tempMeetingRoom

    cntUp = 0
    cntDown = 0
    tempMeetingRoom = 0

    # Tipos de Controladores
    # 0 -> Identificacao do Modelo
    # 1 -> Liga-Desliga
    # 2 -> PI
    # 3 -> Antecipativo
    controllerType = 1