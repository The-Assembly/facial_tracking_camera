import cv2
import serial
import time

frame_w = 640
frame_h = 480

def set_res(cap, x,y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))

#setting up serial connection with Arduino
ser = serial.Serial('COM14', 250000) #Substitute x with your COM port number

time.sleep(2) #Holding the program to establish serial communication

#load the frontal face and profile face classifiers

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
prof_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')

#Creating a VideoCapture object and specifying the device index (i.e which camera)
cap = cv2.VideoCapture(1)

set_res(cap, frame_w,frame_h)

while True:

    #Capture frame-by-frame
    ret,img = cap.read()
    cap.read()
    img = cv2.flip(img, 1)
    
    #Grayscaling the image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Using Equalise Histogram to imporve contrast of image
    gray = cv2.equalizeHist(gray)

    #Applying both classifiers,  the arguments: grayscaled image, scaleFactor which specifies how much the image size is reduced at each image scale, minNeighboura which specifies how many neighbors each candidate rectangle should have to retain it
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)   # faces array stores detected frontal faces 
    profile = prof_cascade.detectMultiScale(gray, 1.3, 5) # profile array stores detected side of the face

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # draws a rectangle around face

    for (x, y, w, h) in profile:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # draws a rectangle around face

    cv2.imshow('img',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
    #Checking if frontal face was detected (by checking length of array)
    
    #if faces array is not empty, frontal face was detected
    if len(faces)!=0:

            #paramers: image, top left corner coordinates, bottom right coordinates, color of the outline for the bounding box, thickness of line
            center_x = (x + (x+w))/2    #computing x coordinate of center of bounding rectangle/face
            center_y = (y + (y+h))/2    #computing y coordinate of center of bounding rectangle/face
            
            err_x = 30*(center_x - frame_w/2)/(frame_w/2)
            err_y = 30*(center_y - frame_h/2)/(frame_h/2)

            #sending it to Arduino via serial communication
            ser.write((str(err_x) + "x!").encode())        #otimizacao: não enviar string, mas inteiro direto
            ser.write((str(err_y) + "y!").encode())        #otimizacao: não enviar string, mas inteiro direto
            print("X: ",err_x," ","Y: ",err_y)

    elif len(profile)!=0:   #if faces array is empty, checks to see if profile face was detected
        
            center_x = (x + (x+w))/2    #computing x coordinate of center of bounding rectangle/face
            center_y = (y + (y+h))/2    #computing y coordinate of center of bounding rectangle/face)
            err_x = 30*(center_x - frame_w/2)/(frame_w/2)
            err_y = 30*(center_y - frame_h/2)/(frame_h/2)
            
            #sending it to Arduino via serial communication
            ser.write((str(err_x) + "x!").encode())        #otimizacao: não enviar string, mas inteiro direto
            ser.write((str(err_y) + "y!").encode())        #otimizacao: não enviar string, mas inteiro direto
            print("X: ",err_x," ","Y: ",err_y)

    else:
       # ser.write("o!".encode())
       print("none")

# release the capture to release the video resources
ser.close()
cap.release()
cv2.destroyAllWindows()
