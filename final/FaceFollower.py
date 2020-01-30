import numpy as np
import cv2
import serial
import random
import sys

very_important_int = 0

# sys.setdefaultencoding('ascii')
# arduino = serial.Serial('COM5', 115200, timeout=.1)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
specs_ori = cv2.imread('scope.png', -1)
xout = 1000
yout = 1000
cap = cv2.VideoCapture(0)
ToBeTrueOrNotToBeTrue = 0
width = cap.get(3)
height = cap.get(4)


def kostil(s):
    nchars = len(s)
    x = sum(ord(s[byte]) << 8 * (nchars - byte - 1) for byte in range(nchars))
    return x


def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape
    rows, cols, _ = src.shape
    y, x = pos[0], pos[1]

    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][0] / 255.0)
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src


while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if format(len(faces)) == "1":
        ToBeTrueOrNotToBeTrue = 1
    elif format(len(faces)) == "0":
        ToBeTrueOrNotToBeTrue = 1
    else:
        ToBeTrueOrNotToBeTrue = 0
    xx = -1
    yy = -1
    for (x, y, w, h) in faces:
        very_important_int = random.randint(1, 4)
        xx = x
        yy = y
        x1 = 0
        x2 = 0
        print('кол-во лиц:', format(len(faces)))
        # if len(faces) == 0:
        #     print(0)
        #     if very_important_int == 1:
        #         cv2.putText(img, "Remove one of these faces", (x - 50, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        #         print(1)
        #     elif very_important_int == 2:
        #         cv2.putText(img, "Remove one of these faces", (x + 50, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        #         print(2)
        #     elif very_important_int == 3:
        #         cv2.putText(img, "Remove one of these faces", (x + 50, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        #         print(3)
        #     elif very_important_int == 4:
        #         cv2.putText(img, "Remove one of these faces", (x - 50, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        #         print(4)
        if ToBeTrueOrNotToBeTrue == 1:
            xpos = (x - width / 2)
            ypos = (y - height / 2)
            xout = round(np.clip(xout + xpos * 16 / width if (abs(ypos) > width / 20) else 0, 0, 2000))
            yout = round(np.clip(yout + ypos * 16 / height if (abs(ypos) > height / 20) else 0, 0, 2000))
            if h > 0 and w > 0:
                # glass_symin = int(y + h / 2)
                # glass_symax = int(y + h)
                glass_symin = int(y)
                glass_symax = int(y + h)
                sh_glass =  glass_symax - glass_symin

                face_glass_roi_color = img[glass_symin:glass_symax, x:x + w]

                specs = cv2.resize(specs_ori, (w, sh_glass), interpolation=cv2.INTER_CUBIC)
                transparentOverlay(face_glass_roi_color, specs)
            cv2.circle(img, (x + w // 2, y + h // 2), (w // 2), (0, 255, 0), 2)
            string = [xx, '|', yy]
            print(x, y)
            # cv2.putText(img, x, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            # cv2.putText(img, y, bottomLeftCornerOfText + 5, font, fontScale, fontColor, lineType)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            # out = (str(round(x / width * 512))[:-2] + 'a' + str(round(y / height * 512))[:-2]+'b')
            # print(out)
            # arduino.write(out.encode())
            'x max = 500, x min = 10, y min = 50, x max = x'
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.line(img, (x + h // 16, y + w // 32), (x + h, y + w), (0, 0, 255), 5)
            cv2.line(img, (x + h // 16, y + w), (x + h, y + w // 32), (0, 0, 255), 5)
            cv2.putText(img, "Remove one of these faces", (x - 200, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    # scale_percent = 20  # Процент от изначального размера
    # width1 = int(img.shape[1] * scale_percent // 100)
    # height1 = int(img.shape[0] * scale_percent // 100)
    # dim = (width, height)
    # resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    # viewImage(resized, "После изменения размера на 20 %")
    # cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    img = cv2.resize(img, (0, 0), fx=3, fy=2.5)
    cv2.imshow('img', img)
    # kek = cv2.IMREAD_COLOR(img, -1)
    # cv2.imshow('img', kek)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
