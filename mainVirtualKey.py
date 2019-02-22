import io
import time
import math
import picamera
import cv2
import cv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import serial,time
ser=serial.Serial("/dev/ttyAMA0",9600)
ser.baudrate=9600

    


    
def processImg(img):
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join my masks
    mask = mask0+mask1

    # set my output img to zero everywhere except my mask
    output_img = img.copy()
    output_img[np.where(mask==0)] = 0
##    cv2.imwrite("output.jpg",output_img)
    # or your HSV image, which I *believe* is what you want
    output_hsv = img_hsv.copy()
    output_hsv[np.where(mask==0)] = 0
    return output_img



def findYLoc(y ):
    flagY = 0
    loc_y = np.array([30, 61, 95, 155, 233 , 306] , dtype = np.uint32)
    if y < loc_y[0] and y > 0:
        print 'Y loc ==> 1'
        flagY = 1
    if y < loc_y[1] and y > loc_y[0]:
        print 'Y loc ==> 2'
        flagY = 2
    if y < loc_y[2] and y > loc_y[1]:
        print 'Y loc ==> 3'
        flagY = 3
    if y < loc_y[3] and y > loc_y[2]:
        print 'Y loc ==> 4'
        flagY = 4
    if y < loc_y[4] and y > loc_y[3]:
        print 'Y loc ==> 5'
        flagY = 5
    return flagY 

def findXLoc(x, flagY):

    loc_x = np.array([    [52 , 122 , 176 , 237 , 300 , 363 , 242 , 485 , 557]  ,
                                    [35 , 100 , 164 , 232 , 300 , 364 , 433 , 502 , 581]  ,
                                    [13 , 85 , 151 , 226 , 300 , 368 , 102 , 515 , 607] ,
                                    [1 , 53 , 130 , 211 , 300 , 368 , 456 , 543 , 640] ,
                                    [1 , 69 , 104 , 197 , 300 , 368 , 477 , 566 , 640] ,
                                    [1 , 69 , 144 , 218 , 300 , 368 , 493 , 566 , 640]  ] , dtype = np.uint32)
    flagX = 0
    if x > loc_x [flagY-1 , 0] and x <= loc_x [flagY-1 , 1]:
            print 'X loc ==> 1'
            flagX = 1
    if x > loc_x [flagY-1 , 1] and x <= loc_x [flagY-1 , 2]:
            print 'X loc ==> 2'
            flagX = 2
    if x > loc_x [flagY-1 , 2] and x <= loc_x [flagY-1 , 3]:
            print 'X loc ==> 3'
            flagX = 3
    if x > loc_x [flagY-1 , 3] and x <= loc_x [flagY-1 , 4]:
            print 'X loc ==> 4'
            flagX = 4
    if x > loc_x [flagY-1 , 4] and x <= loc_x [flagY-1 , 5]:
            print 'X loc ==> 5'
            flagX = 5
    if x > loc_x [flagY-1 , 5] and x <= loc_x [flagY-1 , 6]:
            print 'X loc ==> 6'
            flagX = 6
    if x > loc_x [flagY-1 , 6] and x <= loc_x [flagY-1 , 7]:
            print 'X loc ==> 7'
            flagX = 7
    if x > loc_x [flagY-1 , 7] and x <= loc_x [flagY-1 , 8]:
            print 'X loc ==> 5'
            flagX = 8
    return flagX

def alphabetMap(flagX,flagY):
    charMap= [   [' ' , '_' , 'z' , ' ' , ' ' , 'y' , 'x' , 'w'] ,
                          ['v' , 'u' , 't' , ' ' , ' ' , 's' , 'r' , 'q'] , 
                          ['p' , 'o' , 'n' , 'm' , 'l' , 'k' , 'j' , 'i'] , 
                          ['h' , 'g' , 'f' , 'e' , 'd' , 'c' , 'b' , 'a'] , 
                          [' ' , '0' , '9' , '8' , '7' , '6' , '5' , ' '] , 
                          [' ' , ' ' , '4' , '3' , '2' , '1' , ' ' , ' '] , ]
    # acces char by ==> charMap[0][2] for 'z'
    print charMap[flagY-1 ][flagX-1]
    ser.write(charMap[flagY-1 ][flagX-1])
    
def cameraCapture():
    # Create the in-memory stream
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = (640,480)#(1024, 768)
        camera.start_preview()
        time.sleep(5)
        camera.capture(stream, format='jpeg')
        camera.stop_preview()
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        image = cv2.imdecode(data, 1)
    cv2.imwrite('inImage.jpg',image)
    return image

def subtrc(img1,img2):
    fin =np.zeros((480,640),dtype=np.uint8)
    for i in range(0,640):
        for j in range(0,480):
            fin[j,i] = img1[j,i] - img2[j,i]
    return fin
    
while True:
    image1 = cameraCapture()
    image1 = processImg(image1)

    Gray_frame = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
    ##    cv2.imwrite('gray_frame.jpg',Gray_frame)

    ret,thresh = cv2.threshold(Gray_frame,180,255,0)
    ##    cv2.imwrite('2.jpg',thresh)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#cv2.RETR_TREE

    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in contours]
    if areas:
        print areas
        max_index = np.argmax(areas)
        cnt=contours[max_index]
    
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(image1,(x,y),(x+w,y+h),(0,255,0),2)
        print x+w/2
        print y+h/2
        flag1 = findYLoc(y+h/2)
        flag2 = findXLoc(x+w/2, flag1)
        alphabetMap(flag2,flag1)
    ##    cv2.imwrite("Show.jpg",image1)
    ##    cv2.imshow("Show",image1)
cv2.waitKey()
cv2.destroyAllWindows()
print 'completed'

