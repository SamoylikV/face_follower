import numpy as np
import cv2
import serial
import random
import sys

# sys.setdefaultencoding('ascii')
# servo = serial.Serial('COM7', 9600, timeout=.1) # расокмеьтить когда будут сервы

face_cascade = cv2.CascadeClassifier('frontalface_default.xml')

specs_ori = cv2.imread('glass.png', -1)

xout = 1000
yout = 1000

cap = cv2.VideoCapture(0)  # когда будет вебка поставить на 1

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
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, 0, (120, 120), (350, 350))
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h),
                          (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]

            xpos = (x - width / 2)
            ypos = (y - height / 2)
            print(xpos, ypos)

            xout = round(np.clip(xout + xpos * 16 / width if (abs(ypos) > width / 20) else 0, 0, 2000))
            yout = round(np.clip(yout + ypos * 16 / height if (abs(ypos) > height / 20) else 0, 0, 2000))
            if h > 0 and w > 0:
                # glass_symin = int(y + h / 2)
                # glass_symax = int(y + h)
                peremenaya_sozdanaya_hz_zachem = h * 2
                glass_symin = int(y + h)
                glass_symax = int(y + 1.5 * h)
                sh_glass =  glass_symax - glass_symin - 100

                face_glass_roi_color = img[glass_symin:glass_symax, x:x + w]

                specs = cv2.resize(specs_ori, (w, sh_glass), interpolation=cv2.INTER_CUBIC)
                transparentOverlay(face_glass_roi_color, specs)
    else:
        # xout = 1000
        # yout = 1000
        pass
    # out = ('#1P' + str(xout + 500)[:-2] + '#2P' + str(yout + 500)[:-2] + 'T100\r\n') # раскоменьтить когда будут сервы
    # print(out) # раскоменьтить когда будут сервы
    # servo.write(out.encode()) # раскоменьтить когда будут сервы
    'x max = 500, x min = 10, y min = 50, y max = 300'

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

# -------------------------------

# def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
#     overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
#     h, w, _ = overlay.shape  # Size of foreground
#     rows, cols, _ = src.shape  # Size of background Image
#     y, x = pos[0], pos[1]  # Position of foreground/overlay image
#
#     # loop over all pixels and apply the blending equation
#     for i in range(h):
#         for j in range(w):
#             if x + i >= rows or y + j >= cols:
#                 continue
#             alpha = float(overlay[i][j][0] / 255.0)  # read the alpha channel
#             src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
#     return src


# while 1:
#     ret, img = cap.read()
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(img, 1.2, 5, 0, (120, 120), (350, 350))
#     for (x, y, w, h) in faces:
# if h > 0 and w > 0:
#     glass_symin = int(y + 1.5 * h / 5)
#     glass_symax = int(y + 2.5 * h / 5)
#     sh_glass = glass_symax - glass_symin
#
#     cigar_symin = int(y + 4 * h / 6)
#     cigar_symax = int(y + 5.5 * h / 6)
#     sh_cigar = cigar_symax - cigar_symin
#
#     face_glass_roi_color = img[glass_symin:glass_symax, x:x + w]
#     face_cigar_roi_color = img[cigar_symin:cigar_symax, x:x + w]
#
#     specs = cv2.resize(specs_ori, (w, sh_glass), interpolation=cv2.INTER_CUBIC)
#     cigar = cv2.resize(cigar_ori, (w, sh_cigar), interpolation=cv2.INTER_CUBIC)
#     transparentOverlay(face_glass_roi_color, specs)
#     transparentOverlay(face_cigar_roi_color, cigar, (int(w / 2), int(sh_cigar / 2)))
#
#     cv2.imshow('img', img)
#
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         cv2.imwrite('img.jpg', img)
#         break
#
# cap.release()
#
# cv2.destroyAllWindows()
