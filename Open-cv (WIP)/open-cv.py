import numpy as np
import cv2
import serial
import random
import sys
very_important_int = 0

# sys.setdefaultencoding('ascii')
# arduino = serial.Serial('COM5', 115200, timeout=.1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

width = cap.get(3)
height = cap.get(4)

# def kostil(s):
#     nchars = len(s)
#     x = sum(ord(s[byte]) << 8 * (nchars - byte - 1) for byte in range(nchars))
#     return x

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    xx = -1
    yy = -1
    for (x, y, w, h) in faces:
        very_important_int += random.randint(0, 999)
        xx = x
        yy = y
        if very_important_int % 2 == 0:
            cv2.rectangle(img, (x, y), (x + w, y + h), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(0,255))
        else:
            cv2.circle(img, (x + w // 2, y + h // 2), (w // 2), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), random.randint(0, 255))
        string = [xx, '|', yy]
        # cv2.putText(img, x, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
        # cv2.putText(img, y, bottomLeftCornerOfText + 5, font, fontScale, fontColor, lineType)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        # out = (str(round(x / width * 512))[:-2] + 'a' + str(round(y / height * 512))[:-2]+'b')
        # print(out)
        # arduino.write(out.encode())
        'x max = 500, x min = 10, y min = 50, x max = x'

    cv2.imshow('img', img)
    # kek = cv2.IMREAD_COLOR(img, -1)
    # cv2.imshow('img', kek)
    k = cv2.waitKey(30) & 0xff
    if k == 30:
        break


cap.release()
cv2.destroyAllWindows()
