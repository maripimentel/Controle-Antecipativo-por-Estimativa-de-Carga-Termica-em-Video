##Controle Antecipativo por Estimativa de Carga Termica em Video
##Biblioteca para Comunicacao com a Camera
##Trabalho de Graduacao
##Versao 2
##Autores:
##    Alexandre Saran
##    Mariana Pimentel

# coding=utf-8

from picamera import PiCamera
from time import sleep
from picamera.array import PiRGBArray

# Inicialize camera object
def InicializeCamera():
    camera = PiCamera()
    camera.resolution = (320, 240) # 320 240
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(320, 240))
    return (camera,rawCapture)

# Start recording and setup the file name
def StartVideo(camera, name):
    camera.start_preview()
    camera.start_recording('../../../Videos/'+name+'.h264')
    return camera

# Stop recording
def StopVideo(camera):
    camera.stop_recording()
    camera.stop_preview()
    return camera
