# This script will detect faces via your webcam.
# Tested with OpenCV3

import cv2
import serial # if you have not already done so
import numpy as np

def set_res(cap, x,y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))

ser = serial.Serial('COM14', 250000)  #abre serial COM3

cap = cv2.VideoCapture(0)

frame_w = 640
frame_h = 480
set_res(cap, frame_w,frame_h)

# Create the haar cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
prof_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    cap.read()
    frame=cv2.flip(frame,1)


    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = np.array([]) 
    faces = faceCascade.detectMultiScale(
        gray,   
        scaleFactor=1.1,
        minNeighbors=20,
        minSize=(30, 30)
        #flags = cv2.CV_HAAR_SCALE_IMAGE
    )
    

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    if ([i for i in faces]):     #testa se tem rosto detectado:                                #testa se string está vazia
        face_center_x = faces[0,0]+faces[0,2]/2
        face_center_y = faces[0,1]+faces[0,3]/2

        err_x = 30*(face_center_x - frame_w/2)/(frame_w/2)
        err_y = 30*(face_center_y - frame_h/2)/(frame_h/2)
        #print("X: ",face_center_x," ","Y: ",face_center_y)
        ser.write((str(err_x) + "x!").encode())        #otimizacao: não enviar string, mas inteiro direto
        ser.write((str(err_y) + "y!").encode())        #otimizacao: não enviar string, mas inteiro direto
        print("X: ",err_x," ","Y: ",err_y)
    else:
        ser.write("o!".encode())        
                     
# When everything done, release the capture
ser.close()
cap.release()
cv2.destroyAllWindows()