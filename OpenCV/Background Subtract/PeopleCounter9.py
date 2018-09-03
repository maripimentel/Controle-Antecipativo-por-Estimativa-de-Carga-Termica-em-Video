##Identificação e Contagem do Número de Pessoas por Vídeo
##Programa Prinpipal
##Trabalho de Graduação 1
##Versão 1
##Autores:
##    Alexandre Saran
##    Mariana Pimentel
##Baseado no Material de: Federico Mejia

import numpy as np
import cv2
import MyPerson
import time
import sys

#Contadores de entrada e saída
cnt_up   = 0
cnt_down = 0

#Caminho para salvar os resultados no Raspberry Pi
path = '/home/pi/Documents/OpenCV/Background Subtract/Result'

#Nome do vídeo como input do terminal
video_name = sys.argv[1]
cap = cv2.VideoCapture(video_name + '.avi') #Open video file

#Impressão da propriedades do vídeo
for i in range(19):
    print (i, cap.get(i))

#Cálculo da área limite para definição se é ou não pessoa
#Esse valor deve ser ajustado dependendo do ambiente
w = cap.get(3)
h = cap.get(4)
frameArea = h*w
areaTH = frameArea/250
print ('Area Threshold', areaTH)

#Definição das linhas de entrada e de saída
line_up = int(2*(h/5))
line_down   = int(3*(h/5))

#LInhas a partir das quais a mémoria pode ser liberada
up_limit =   int(1*(h/5))
down_limit = int(4*(h/5))

print ("Red line y:",str(line_down))
print ("Blue line y:", str(line_up))
line_down_color = (255,0,0)
line_up_color = (0,0,255)
pt1 =  [0, line_down];
pt2 =  [w, line_down];
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 =  [0, line_up];
pt4 =  [w, line_up];
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 =  [0, up_limit];
pt6 =  [w, up_limit];
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 =  [0, down_limit];
pt8 =  [w, down_limit];
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

#Cria o subtrator de fundo
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

#Elementos necessários para a aplicação de filtros e trasformações morfológicas
kernelOp = np.ones((3,3),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelCl = np.ones((11,11),np.uint8)

#Variáveis
font = cv2.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1

cont = 1
while(cap.isOpened()):
##Para um vídeo contínuo camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
    
    #Lê um frame do vídeo
    ret, frame = cap.read()

    for i in persons:
        i.age_one()
        
    #########################
    #   PRÉ-PROCESSAMENTO   #
    #########################
    
    #Aplica sa subtração de fundo
    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)
    
    name_img_original = path + '/' + video_name + '_' + str(cont) + '_original.jpg'
    name_img_sub = path + '/' + video_name + '_' + str(cont) + '_subtractor.jpg'
    cv2.imwrite(name_img_original,frame)
    cv2.imwrite(name_img_sub,fgmask)

    try:
        #Eliminação das sombras com a transformação binária
        ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        ret,imBin2 = cv2.threshold(fgmask2,200,255,cv2.THRESH_BINARY)
        #Abertura para tirar ruído
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)
        #Fechamento para juntar regiões brancas
        mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)
        
        name_img_transf = path + '/' + video_name + '_' + str(cont) + '_transformation.jpg'
        cv2.imwrite(name_img_transf,mask)
    except:
        print('EOF')
        print ('UP:',cnt_up)
        print ('DOWN:',cnt_down)
        break
    
    #################
    #   CONTORNOS   #
    #################
    
    _, contours0, hierarchy = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours0:
        area = cv2.contourArea(cnt)
        if area > areaTH:
    
            #####################
            #   RASTREAMENTO    #
            #####################
            
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)

            new = True
            if cy in range(up_limit,down_limit):
                for i in persons:
                    if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:
                        # Pessoa próxima a uma pessoa já detectada
                        new = False
                        i.updateCoords(cx,cy)   #Atualiza
                        if i.going_UP(line_down,line_up) == True:
                            cnt_up += 1;
                            print("ID:",i.getId(),'crossed going up at',time.strftime("%c"))
                        elif i.going_DOWN(line_down,line_up) == True:
                            cnt_down += 1;
                            print("ID:",i.getId(),'crossed going down at',time.strftime("%c"))
                        break
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > down_limit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < up_limit:
                            i.setDone()
                    if i.timedOut():
                        #Se tiver timeout retirar pessoa da lista
                        index = persons.index(i)
                        persons.pop(index)
                        del i     
                if new == True:
                    p = MyPerson.MyPerson(pid,cx,cy, max_p_age)
                    persons.append(p)
                    pid += 1
                    
            ##############################
            #   DESENHOS DAS PESSOAS     #
            ##############################
            
            cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            name_img_rectangle = path + '/' + video_name + '_' + str(cont) + '_rectangle.jpg'
            cv2.imwrite(name_img_rectangle,img)
            
            img_contours = cv2.drawContours(frame, cnt, -1, (0,255,0), 3)
            name_img_cont = path + '/' + video_name + '_' + str(cont) + '_contours.jpg'
            cv2.imwrite(name_img_cont,img_contours)
            
    #############################
    # DESENHOS DAS TRAJETÓRIAS  #
    ############################
    for i in persons:
##        if len(i.getTracks()) >= 2:
##            pts = np.array(i.getTracks(), np.int32)
##            pts = pts.reshape((-1,1,2))
##            frame = cv2.polylines(frame,[pts],False,i.getRGB())
##        if i.getId() == 9:
##            print str(i.getX()), ',', str(i.getY())
        cv2.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv2.LINE_AA)
        
    #################
    #    IMAGENS    #
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
    name_img_final = path + '/' + video_name + '_' + str(cont) + '_final.jpg'
    cv2.imwrite(name_img_final,frame)
    cont+=1
    #cv2.imshow('Mask',mask)    
    
    #Se pressionarem ESC, pare
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
#################
#    LIMPEZA    #
#################
cap.release()
cv2.destroyAllWindows()