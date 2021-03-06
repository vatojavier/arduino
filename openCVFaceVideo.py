import numpy as np
import cv2
import serial
import struct


def punto_medio(x, y, w, h):
    return int((x+w)/2), int((y+h)/2)


cap = cv2.VideoCapture('pruebaMovil.mp4')
esclado = 20

face_cascade = cv2.CascadeClassifier('/home/javi/Desktop/OpenCV-tmp/opencv-3/data/haarcascades/'
                                     'haarcascade_frontalface_default.xml')

# ser = serial.Serial('/dev/ttyACM0', baudrate=9600)

string = ''

prueba = 280
pm_x = 100
pm_y = 100
string_x = ''

pillar = False
pillar_todos = False

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(str(width) + "x" + str(height))

while cap.isOpened():


    try:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if pillar is False:
            pillar = True
        else:
            pillar = False

        if pillar or pillar_todos:
            width = int(frame.shape[1] * esclado / 100)
            height = int(frame.shape[0] * esclado / 100)
            dim = (width, height)

            # resize image
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            #frame = cv2.resize(frame, (300, 300))


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

                print(str(pm_x) + "\t" + str(pm_y) + "\n")
                string_x = str(pm_x*1.5)
                # ser.write(string_x.encode('utf-8'))

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
        # ser.close()
