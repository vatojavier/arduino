import numpy as np
import cv2
import serial
import struct


def punto_medio(x_c, y_c, w_c, h_c):
    return int(x_c + (w_c / 2)), int(y_c + (h_c / 2))


def pos_ref(xf, wid):
    print("Pos->>>>>" + str(xf))

    if xf < wid/2 - precision_x:
        return IZQ
    elif xf > (wid/2 + precision_x):
        return DER
    else:
        return CENTR


cap = cv2.VideoCapture(2)

IZQ = "1"
CENTR = "2"
DER = "3"

if not cap.isOpened():
    print("No se puede abrir la camara\n")

face_cascade = cv2.CascadeClassifier('/home/javi/Desktop/OpenCV-tmp/opencv-3/data/haarcascades/'
                                     'haarcascade_frontalface_default.xml')

ser = serial.Serial('/dev/ttyACM0', baudrate=250000)

string = ''

prueba = 280
pm_x = 100
pm_y = 100
string_x = ''

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

precision_x = 50

while True:

    try:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.line(frame, ((x + int(w / 2)), y), ((x + int(w / 2)), y + h), 1, 2)
            cv2.line(frame, (x, y + int(h / 2)), (x + w, y + int(h / 2)), 1, 2)

            pm_x, pm_y = punto_medio(x, y, w, h)
            pos_cara = pos_ref(pm_x, width)
            ser.write(pos_cara.encode('utf-8'))

        # Dibujando linea central
        cv2.line(frame, (int(width/2 - precision_x), int(height/2)),
                 (int(width/2 + precision_x), int(height/2))
                 , (255, 0, 0), 1)

        # Display the resulting frame
        cv2.imshow('img', frame)
        string = ''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except KeyboardInterrupt:
        # When everything done, release the capture
        print("Cerrando")
        cap.release()
        cv2.destroyAllWindows()
        ser.close()
