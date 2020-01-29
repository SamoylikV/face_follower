import numpy as np
import cv2
import serial
import random
import sys

# sys.setdefaultencoding('ascii')
servo = serial.Serial('COM7', 9600, timeout=.1)


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')




xout = 1000
yout = 1000

cap = cv2.VideoCapture(1)

width = cap.get(3)
height = cap.get(4)

def kostil(s):
    nchars = len(s)
    x = sum(ord(s[byte]) << 8 * (nchars - byte - 1) for byte in range(nchars))
    return x

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces)>0:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

            xpos = (x-width/2)
            ypos = (y-height/2)
            print(xpos, ypos)

            xout = round(np.clip(xout + xpos * 16 / width if (abs(ypos) > width / 20) else 0, 0, 2000))
            yout = round(np.clip(yout + ypos * 16 / height if (abs(ypos) > height / 20) else 0, 0, 2000))
    else:
        #xout = 1000
        #yout = 1000
        pass
    out = ('#1P' + str(xout + 500)[:-2] + '#2P' + str(yout+500)[:-2] + 'T100\r\n')
    print(out)
    servo.write(out.encode())
    'x max = 500, x min = 10, y min = 50, x max = x'


    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
