import numpy as np
import cv2
import serial
import random
import sys

# sys.setdefaultencoding('ascii')
servo = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

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

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        x = ((x - width) * 2000 / width)
        y = ((y - height) * 2000 / height)
        out = ('#1P' + str(round(x + 500))[:-2] + '#2P' + str(round(y))[:-2] + 'T100\r\n')
        print(out)
        servo.write(out.encode())
        'x max = 500, x min = 10, y min = 50, x max = x'

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
