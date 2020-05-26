import numpy as np
import cv2
import serial
import time
import concurrencia


# Punto medio del cuadrado (x,y)
def punto_medio(x_c, y_c, w_c, h_c):
    return int(x_c + (w_c / 2)), int(y_c + (h_c / 2))


# devuelve si esta DER IZQ o CENT de
def pos_ref(xf, wid):

    if xf < wid/2 - precision_x:
        return IZQ
    elif xf > (wid/2 + precision_x):
        return DER
    else:
        return CENTR


# Envia al arduino la posicion relativa de la cara
def enviar_pos_ref(pos):
    ser.write(pos.encode('utf-8'))


# Dibuja la lina de preicision
def dibujar_linea_precision():
    # Dibujando linea central
    cv2.line(frame, (int(width / 2 - precision_x), int(height / 2)),
             (int(width / 2 + precision_x), int(height / 2))
             , (255, 0, 0), 1)


escalar = True
esclado = 90
precision_x = 50

for i in range(1,30):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(i)
            break

IZQ = "1"
CENTR = "2"
DER = "3"

if not cap.isOpened():
    print("No se puede abrir la camara\n")
    exit()

face_cascade = cv2.CascadeClassifier('/home/javi/Desktop/OpenCV-tmp/opencv-3/data/haarcascades/'
                                     'haarcascade_frontalface_default.xml')

# ser = serial.Serial('/dev/ttyACM0', baudrate=2000000)

pm_x = 100
pm_y = 100

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(str(width) + "x" + str(height))

while True:

    try:
        # Capture frame-by-frame
        ret, frame = cap.read()
        start = time.time()

        if escalar:
            width = int(frame.shape[1] * esclado / 100)
            height = int(frame.shape[0] * esclado / 100)
            dim = (width, height)

            # resize image
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

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
            # enviar_pos_ref(pos_cara)

        dibujar_linea_precision()

        # Display the resulting frame
        cv2.imshow('img', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        end = time.time()
        print(end - start)

    except KeyboardInterrupt:
        # When everything done, release the capture
        print("Cerrando")
        cap.release()
        cv2.destroyAllWindows()
        ser.close()
