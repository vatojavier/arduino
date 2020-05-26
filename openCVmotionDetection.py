from imutils.video import VideoStream
from datetime import datetime
import cv2
import argparse
import imutils
import time
import serial


# Punto medio del cuadrado (x,y)
def punto_medio(x_c, y_c, w_c, h_c):
    return int(x_c + (w_c / 2)), int(y_c + (h_c / 2))


def enviar_pos_ref(pos_x, pos_y):
    str_pos = pos_x + "-" + pos_y + "\n"
    print(str_pos)
    ser.write(str_pos.encode('utf-8'))


ser = serial.Serial('/dev/ttyACM0', baudrate=2000000)

# parse command-line the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the .mp4 file")
ap.add_argument("-a", "--min-area", type=int, default=1000, help="minimum motion area")

# convert to dictionary
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from the camera
if args.get("video", None) is None:
    video = VideoStream(src=2).start()
    time.sleep(3.0)

# otherwise, we are reading from a video file
else:
    video = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
first_frame = None

# initial and the last state
states = [None, None]


# loop over the frames of the video
while True:
    # grab the current frame and initialize state
    # TODO: Optimize framerate
    frame = video.read()
    frame = frame if args.get("video", None) is None else frame[1]
    state = 0

    # if the frame could not be grabbed, then we have reached the end of the video
    if frame is None:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayscale_frame = cv2.GaussianBlur(grayscale_frame, (21, 21), 0)

    # if the first frame is None, initialize it
    if first_frame is None:
        first_frame = grayscale_frame
        continue

    # compute the absolute difference between current and the first frame
    delta_frame = cv2.absdiff(first_frame, grayscale_frame)

    # compute the threshold frame 50,255
    thresh_frame = cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded frame, then find contours
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=3)
    contours = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]

    previos_area = -1
    selected_contour = -1
    selected = False

    # loop through the contours we found
    for c in contours:
        # ignore small contours
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # selecting just one contour to send to the serial
        if selected is False:
            selected_contour = c
            selected = True
        else:
            if cv2.contourArea(c) > cv2.contourArea(selected_contour):
                selected_contour = c

        # draw rectangle for the contour
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        state = 1

    if selected is True:
        (x, y, w, h) = cv2.boundingRect(selected_contour)
        pm_x, pm_y = punto_medio(x, y, w, h)

        enviar_pos_ref(str(pm_x), str(pm_y))

    # add the state of the current frame
    states.append(state)
    states = states[-2:]

    # draw the state and current date and time on the frame
    cv2.putText(frame, "State: {}".format(state), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, datetime.now().strftime("%d/%m/%Y %I:%M:%S"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame layers, each in separate window
    cv2.imshow("Gray Frame", grayscale_frame)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Native Frame", frame)

    key = cv2.waitKey(1) & 0xFF

    # if 'q' is pressed, break the loop, no funciona
    if key == ord('q'):
        break


# FIXME: Threading issue
# in linux csv serialization both with camera stopping
# may cause "FATAL: exeption not rethrown" (OpenCV threading issue?)
# Temporary fix using time.sleep() works well
time.sleep(3.0)

# cleanup the camera and destroy windows
video.stop() if args.get("video", None) is None else video.release()
cv2.destroyAllWindows()
