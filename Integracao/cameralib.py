##Controle Antecipativo por Estimativa de Carga Termica em Video
##Biblioteca para Comunicacao com a Camera
##Trabalho de Graduacao
##Versao 1
##Autores:
##    Alexandre Saran
##    Mariana Pimentel

# coding=utf-8

from picamera import PiCamera
from time import sleep

# Inicialize camera object
def InicializeCamera():
	camera = PiCamera()
	return camera

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