import serial
import time
import struct
import serial.tools.list_ports
import settings
from scipy import signal
from simple_pid import PID

TEMP = 23.0

Kp = 0.12
Ki = 13 * Kp

piController = PID (-Kp, -Ki, 0, setpoint = TEMP)

print(piController.Kp)
print(piController.Ki)
print(piController.Kd)
print(piController.setpoint)
            