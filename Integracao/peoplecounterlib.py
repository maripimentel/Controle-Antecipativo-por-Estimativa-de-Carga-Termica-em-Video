##Controle Antecipativo por Estimativa de Carga Termica em Video
##Biblioteca para Identificacao e Contagem do Numero de Pessoas por Video
##Trabalho de Graduacao
##Versao 10
##Autores:
##    Alexandre Saran
##    Mariana Pimentel
##Baseado no Material de: Federico Mejia

# coding=utf-8

import numpy as np
import cv2
import personlib
import time
import sys

from picamera import PiCamera
from cameralib import *
import os

def PeopleCounter(cnt_up, cnt_down, name, saveResults):
    TAG = '(peoplecouterlib) '

    if(saveResults):
        # Result's path on Raspberry Pi
        path = '../../Resultados/'+name
        video_name = name

        print(TAG+'caminho: '+ str(path))
        print(TAG+'nome do video: '+ str(video_name))
        
        if not os.path.exists(path):
            os.makedirs(path)

    # Initialize the camera and grab a reference to the raw camera capture
    (camera,rawCapture) = InicializeCamera()

    # Allow the camera to warmup
    time.sleep(0.1)

    # Calculate the threshold to define if it is or not a person
    w = 640
    h = 480
    frameArea = h*w
    areaTH = frameArea/250
    print(TAG+'threshold:'+str(areaTH))

    # Define up and down line
    line_up = int(2*(h/5))
    line_down = int(3*(h/5))

    # After this lines memory can be free
    up_limit = int(1*(h/5))
    down_limit = int(4*(h/5))

    # Calculate important points
    print(TAG+"y da linha inferior:"+str(line_down))
    print(TAG+"y da linha superior:"+str(line_up))
    line_down_color = (255,0,0)
    line_up_color = (0,0,255)

    (pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8) = calculatePoints(w, line_up, line_down, up_limit, down_limit)
    (pts_L1, pts_L2, pts_L3, pts_L4) = calculateLinePoints(pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8)

    # Creates the backgroud subtractor
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

    # Necessary to apply filters and morfological transforms
    kernelOp = np.ones((3,3),np.uint8)
    kernelOp2 = np.ones((5,5),np.uint8)
    kernelCl = np.ones((11,11),np.uint8)

    persons = []
    max_p_age = 5
    pid = 1

    cont = 1
    for cap in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Para um video continuo camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
        
        # Read a frame
        frame = cap.array

        for i in persons:
            i.age_one()
            
        #########################
        #      PRE-PROCESS      #
        #########################
        
        # Apply background subtraction
        fgmask = fgbg.apply(frame)
        fgmask2 = fgbg.apply(frame)

        saveSubtractorImages(saveResults, path, video_name, cont, frame, fgmask)

        try:
            (mask, mask2) = preProcess(fgmask, fgmask2, saveResults, path, video_name, cont)
        except:
            print (TAG+'para cima: ',cnt_up)
            print (TAG+'para baixo: ',cnt_down)
            break
        
        #################
        #    CONTOURS   #
        #################
        
        _, contours0, hierarchy = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours0:
            area = cv2.contourArea(cnt)
            if area > areaTH:
        
                #####################
                #     TRACKING      #
                #####################
                
                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                x,y,w,h = cv2.boundingRect(cnt)

                new = True
                if cy in range(up_limit,down_limit):
                    for i in persons:
                        (i, persons, cnt_up, cnt_down, stopLoop, new) = defineDirection(i, cx, cy, w, h, new, cnt_up, cnt_down, line_up, line_down, up_limit, down_limit, persons, TAG)
                        if (stopLoop):
                            break

                    if new == True:
                        p = personlib.MyPerson(pid,cx,cy, max_p_age)
                        persons.append(p)
                        pid += 1
                        
                
                # Drawing persons
                drawPersons(frame, cx, cy, x, y, w, h, saveResults, path, video_name, cnt)
                
        # Drawing tracking
        drawTrack(frame, persons, cnt_up, cnt_down, line_down_color, line_up_color, pts_L1, pts_L2, pts_L3, pts_L4, saveResults, path, video_name, cont)
        
        cont+=1 
        
        #If ESC is pressed, stop
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        rawCapture.truncate(0)
        
    #################
    #     CLEAR     #
    #################
##    cap.release()
    
    cv2.destroyAllWindows()

    return cnt_up - cnt_down

def calculatePoints(w, line_up, line_down, up_limit, down_limit):
    pt1 =  [0, line_down];
    pt2 =  [w, line_down];

    pt3 =  [0, line_up];
    pt4 =  [w, line_up];

    pt5 =  [0, up_limit];
    pt6 =  [w, up_limit];
    
    pt7 =  [0, down_limit];
    pt8 =  [w, down_limit];

    return (pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8)

def calculateLinePoints(pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8):
    pts_L1 = np.array([pt1,pt2], np.int32)
    pts_L1 = pts_L1.reshape((-1,1,2))

    pts_L2 = np.array([pt3,pt4], np.int32)
    pts_L2 = pts_L2.reshape((-1,1,2))

    pts_L3 = np.array([pt5,pt6], np.int32)
    pts_L3 = pts_L3.reshape((-1,1,2))

    pts_L4 = np.array([pt7,pt8], np.int32)
    pts_L4 = pts_L4.reshape((-1,1,2))

    return (pts_L1, pts_L2, pts_L3, pts_L4)

def drawTrack(frame, persons, cnt_up, cnt_down, line_down_color, line_up_color, pts_L1, pts_L2, pts_L3, pts_L4, saveResults, path, video_name, cont):
    font = cv2.FONT_HERSHEY_SIMPLEX

    for i in persons:
        cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)
            
    #################
    #     IMAGES    #
    #################
    str_up = 'UP: '+ str(cnt_up)
    str_down = 'DOWN: '+ str(cnt_down)
    frame = cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
    frame = cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
    frame = cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
    frame = cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
    cv2.putText(frame, str_up ,(10,40),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, str_up ,(10,40),font,0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(frame, str_down ,(10,90),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, str_down ,(10,90),font,0.5,(255,0,0),1,cv2.LINE_AA)

    cv2.imshow('Frame',frame)

    if (saveResults):
        name_img_final = path + '/' + video_name + '_' + str(cont) + '_final.jpg'
        cv2.imwrite(name_img_final,frame)

def drawPersons(frame, cx, cy, x, y, w, h, saveResults, path, video_name, cnt):
    cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
    img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    if (saveResults):
        name_img_rectangle = path + '/' + video_name + '_' + str(cont) + '_rectangle.jpg'
        cv2.imwrite(name_img_rectangle,img)
    
    img_contours = cv2.drawContours(frame, cnt, -1, (0,255,0), 3)

    if (saveResults):
        name_img_cont = path + '/' + video_name + '_' + str(cont) + '_contours.jpg'
        cv2.imwrite(name_img_cont,img_contours)

def saveSubtractorImages(saveResults, path, video_name, cont, frame, fgmask):
    if(saveResults):
        name_img_original = path + '/' + video_name + '_' + str(cont) + '_original.jpg'
        name_img_sub = path + '/' + video_name + '_' + str(cont) + '_subtractor.jpg'
        cv2.imwrite(name_img_original,frame)
        cv2.imwrite(name_img_sub,fgmask)

def preProcess(fgmask, fgmask2, saveResults, path, video_name, cont):

    # Eliminate shadows
    ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
    ret,imBin2 = cv2.threshold(fgmask2,200,255,cv2.THRESH_BINARY)

    # Eliminate noise
    mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
    mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)

    # Join white parts
    mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)
    
    name_img_transf = path + '/' + video_name + '_' + str(cont) + '_transformation.jpg'
    cv2.imwrite(name_img_transf,mask)

    return (mask, mask2)

def  defineDirection(i, cx, cy, w, h, new, cnt_up, cnt_down, line_up, line_down, up_limit, down_limit, persons, TAG):
    stopLoop = False

    if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:
        # Close to a person already detected
        new = False
        i.updateCoords(cx,cy)   #Refresh
        if i.going_UP(line_down,line_up) == True:
            cnt_up += 1;
            print(TAG+str(i.getId()) +' foi para cima aos '+time.strftime("%c"))
        elif i.going_DOWN(line_down,line_up) == True:
            cnt_down += 1;
            print(TAG+str(i.getId()) +' foi para baixo aos '+time.strftime("%c"))
        stopLoop = True
    if i.getState() == '1':
        if i.getDir() == 'down' and i.getY() > down_limit:
            i.setDone()
        elif i.getDir() == 'up' and i.getY() < up_limit:
            i.setDone()
    if i.timedOut():
        # If it reaches timeout, remove person from list
        index = persons.index(i)
        persons.pop(index)
        del i    

    return (i, persons, cnt_up, cnt_down, stopLoop, new)

