# -*- coding: utf-8 -*-
import os, sys
import cv2
 
cap = cv2.VideoCapture('/home/zhaosl/python_project/video2images/inputvideo/21.avi')
i = 1 
ret = True                 
while(True and ret):
     ret, frame = cap.read()
     print ret 
     #path = '/cvg_2/hadmap/%06d.jpg' % (i) 
     path = '/home/zhaosl/python_project/video2images/outputimages/21/%08d.jpg' % (i)
     i = i + 1
#cv2.circle(frame,(343,237+50),10,(0,255,255),-1)
#     cv2.ellipse(frame,(343,237+50),(150,100),0,240,300,(255,0,0),-1)
     if(ret):
         cv2.imwrite(path,frame)
cap.release()                                     
