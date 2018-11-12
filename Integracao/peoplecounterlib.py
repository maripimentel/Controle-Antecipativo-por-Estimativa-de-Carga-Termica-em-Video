##Controle Antecipativo por Estimativa de Carga Termica em Video
##Biblioteca para Identificacao e Contagem do Numero de Pessoas por Video
##Trabalho de Graduacao
##Versao 10
##Autores:
##    Alexandre Saran
##    Mariana Pimentel
##Baseado no Material de: Federico Mejia

# coding=utf-8

from cameralib import *
import settings
import numpy as np
import cv2
import personlib
import time
import datetime
import sys
import os

def PeopleCounter(cntUp, cntDown, name, saveResults):
    TAG = '(peoplecouterlib) '

    # Result's path on Raspberry Pi
    path = '../../Resultados/'+name
    videoName = name
    
    print(TAG+'caminho: '+ str(path))
    print(TAG+'nome do video: '+ str(videoName))
        
    if(saveResults):
        if not os.path.exists(path):
            os.makedirs(path)

    # Initialize the camera and grab a reference to the raw camera capture
    (camera,rawCapture) = InicializeCamera()
    settings.camera = camera

    # Allow the camera to warmup
    time.sleep(0.1)

    # Calculate the threshold to define if it is or not a person
    w = 320
    h = 240
    frameArea = h*w
    #areaTH = frameArea/250
    areaTH = frameArea/60
    areaTHSuperior = frameArea/3
    print(TAG+'threshold:'+str(areaTH))

    # Define up and down line
    #lineUp = int(2*(h/5))
    #lineDown = int(3*(h/5))
    lineUp = int(13*(h/20))
    lineDown = int(13*(h/20))
    
    # After this lines memory can be free
    #upLimit = int(1*(h/5))
    #downLimit = int(4*(h/5))
    upLimit = int(2*(h/20))
    downLimit = int(18*(h/20))

    # Calculate important points
    print(TAG+"y da linha inferior:"+str(lineDown))
    print(TAG+"y da linha superior:"+str(lineUp))
    lineDownColor = (255,0,0)
    lineUpColor = (0,0,255)

    (pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8) = calculatePoints(w, lineUp, lineDown, upLimit, downLimit)
    (ptsL1, ptsL2, ptsL3, ptsL4) = calculateLinePoints(pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8)

    # Creates the backgroud subtractor
    fgbg = cv2.createBackgroundSubtractorMOG2(history = 500, varThreshold = 16, detectShadows = False)

    # Necessary to apply filters and morfological transforms
    kernelOp = np.ones((5,5),np.uint8)
    kernelOp2 = np.ones((7,7),np.uint8)
    kernelCl = np.ones((11,11),np.uint8)

    persons = []
    maxPAge = 5
    pid = 1

    cont = 1
    for cap in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Para um video continuo camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
        settings.cntDown = cntDown
        settings.cntUp = cntUp
        
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

        saveSubtractorImages(saveResults, path, videoName, cont, frame, fgmask)

        try:
            (mask, mask2) = preProcess(fgmask, fgmask2, saveResults, path, videoName, cont, kernelOp, kernelCl)
        except:
            print (TAG+'para cima: '+str(cntUp))
            print (TAG+'para baixo: '+str(cntDown))
            break
        
        #################
        #    CONTOURS   #
        #################
        
        _, contours0, hierarchy = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours0:
            area = cv2.contourArea(cnt)
            if area > areaTH and area < areaTHSuperior:
        
                #####################
                #     TRACKING      #
                #####################
                
                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                x,y,w,h = cv2.boundingRect(cnt)

                new = True
                if cy in range(upLimit,downLimit):
                    for i in persons:
                        (i, persons, cntUp, cntDown, stopLoop, new) = defineDirection(i, cx, cy, w, h, new, cntUp, cntDown, lineUp, lineDown, upLimit, downLimit, persons, TAG)
                        if i.timedOut():
                            # If it reaches timeout, remove person from list
                            index = persons.index(i)
                            persons.pop(index)
                            del i  
                        if (stopLoop):
                            break

                    if new == True:
                        p = personlib.MyPerson(pid,cx,cy, maxPAge)
                        persons.append(p)
                        pid += 1
                        
                
                # Drawing persons
                drawPersons(frame, cx, cy, x, y, w, h, saveResults, path, videoName, cont, cnt)
        
        timestamp = time.time()
        dateTime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
        
        dateTimeHour = dateTime.split('_')[1]
        hour = dateTimeHour.split('-')[0]
        
        if(cntUp - cntDown + settings.initialNumPeople < 0):
            cntUp = settings.cntUp;
            cntDown = settings.cntDown;
            
        nightHours = ['23', '00', '01', '02', '03', '04', '05', '06']
        if(hour in nightHours):
            if(settings.initialNumPeople != cntDown - cntUp):
                cntDown = cntUp + settings.initialNumPeople
        
        # Drawing tracking
        drawTrack(frame, persons, cntUp, cntDown, lineDownColor, lineUpColor, ptsL1, ptsL2, ptsL3, ptsL4, saveResults, path, videoName, cont)
        
        cont+=1 
        
        #If ESC is pressed, stop
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            camera.close()
            break
        
        rawCapture.truncate()
        rawCapture.seek(0)
        
    #################
    #     CLEAR     #
    #################
##    cap.release()
    
    cv2.destroyAllWindows()

    # return cntUp - cntDown

def calculatePoints(w, lineUp, lineDown, upLimit, downLimit):
    pt1 =  [0, lineDown];
    pt2 =  [w, lineDown];

    pt3 =  [0, lineUp];
    pt4 =  [w, lineUp];

    pt5 =  [0, upLimit];
    pt6 =  [w, upLimit];
    
    pt7 =  [0, downLimit];
    pt8 =  [w, downLimit];

    return (pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8)

def calculateLinePoints(pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8):
    ptsL1 = np.array([pt1,pt2], np.int32)
    ptsL1 = ptsL1.reshape((-1,1,2))

    ptsL2 = np.array([pt3,pt4], np.int32)
    ptsL2 = ptsL2.reshape((-1,1,2))

    ptsL3 = np.array([pt5,pt6], np.int32)
    ptsL3 = ptsL3.reshape((-1,1,2))

    ptsL4 = np.array([pt7,pt8], np.int32)
    ptsL4 = ptsL4.reshape((-1,1,2))

    return (ptsL1, ptsL2, ptsL3, ptsL4)

def drawTrack(frame, persons, cntUp, cntDown, lineDownColor, lineUpColor, ptsL1, ptsL2, ptsL3, ptsL4, saveResults, path, videoName, cont):
    font = cv2.FONT_HERSHEY_SIMPLEX

    for i in persons:
        cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)
            
    #################
    #     IMAGES    #
    #################
    strUp = 'UP: '+ str(cntUp)
    strDown = 'DOWN: '+ str(cntDown)
    frame = cv2.polylines(frame,[ptsL1],False,lineDownColor,thickness=2)
    frame = cv2.polylines(frame,[ptsL2],False,lineUpColor,thickness=2)
    frame = cv2.polylines(frame,[ptsL3],False,(255,255,255),thickness=1)
    frame = cv2.polylines(frame,[ptsL4],False,(255,255,255),thickness=1)
    cv2.putText(frame, strUp ,(10,40),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, strUp ,(10,40),font,0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(frame, strDown ,(10,90),font,0.5,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(frame, strDown ,(10,90),font,0.5,(255,0,0),1,cv2.LINE_AA)

    cv2.imshow('Frame',frame)

    if (saveResults):
        nameImgFinal = path + '/' + videoName + '_' + str(cont) + '_final.jpg'
        cv2.imwrite(nameImgFinal,frame)

def drawPersons(frame, cx, cy, x, y, w, h, saveResults, path, videoName, cont, cnt):
    cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
    img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    if (saveResults):
        nameImgRectangle = path + '/' + videoName + '_' + str(cont) + '_rectangle.jpg'
        cv2.imwrite(nameImgRectangle,img)
    
    imgContours = cv2.drawContours(frame, cnt, -1, (0,255,0), 3)

    if (saveResults):
        nameImgCont = path + '/' + videoName + '_' + str(cont) + '_contours.jpg'
        cv2.imwrite(nameImgCont,imgContours)

def saveSubtractorImages(saveResults, path, videoName, cont, frame, fgmask):
    if(saveResults):
        nameImgOriginal = path + '/' + videoName + '_' + str(cont) + '_original.jpg'
        nameImgSub = path + '/' + videoName + '_' + str(cont) + '_subtractor.jpg'
        cv2.imwrite(nameImgOriginal,frame)
        cv2.imwrite(nameImgSub,fgmask)

def preProcess(fgmask, fgmask2, saveResults, path, videoName, cont, kernelOp, kernelCl):

    # Eliminate shadows
    ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
    ret,imBin2 = cv2.threshold(fgmask2,200,255,cv2.THRESH_BINARY)
    #ret,imBin= cv2.threshold(fgmask,0,255,cv2.THRESH_BINARY+cv.THRESH_OTSU)
    #ret,imBin2 = cv2.threshold(fgmask2,0,255,cv2.THRESH_BINARY+cv.THRESH_OTSU)

    # Eliminate noise
    mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
    mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)

    # Join white parts
    mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)
    
    if(saveResults):
        nameImgTransf = path + '/' + videoName + '_' + str(cont) + '_transformation.jpg'
        cv2.imwrite(nameImgTransf,mask)

    return (mask, mask2)

def defineDirection(i, cx, cy, w, h, new, cntUp, cntDown, lineUp, lineDown, upLimit, downLimit, persons, TAG):
    stopLoop = False
    if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:
        # Close to a person already detected
        lineLeft = int(8*(320/10))
        lineRight = int(3*(320/10))
    
        new = False
        i.updateCoords(cx,cy)   #Refresh
        if i.going_UP(lineDown,lineUp,lineLeft,lineRight) == True:
            cntUp += 1;
            print(TAG+str(i.getId()) +' foi para cima aos '+time.strftime("%c"))
        elif i.going_DOWN(lineDown,lineUp,lineLeft,lineRight) == True:
            cntDown += 1;
            print(TAG+str(i.getId()) +' foi para baixo aos '+time.strftime("%c"))
        stopLoop = True
    if i.getState() == '1':
        if i.getDir() == 'down' and i.getY() > downLimit:
            i.setDone()
        elif i.getDir() == 'up' and i.getY() < upLimit:
            i.setDone()  

    return (i, persons, cntUp, cntDown, stopLoop, new)

