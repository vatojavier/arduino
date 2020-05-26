
import serial
from time import sleep


def enviar_pos_ref(pos_x, pos_y):
    str_pos = pos_x + "-" + pos_y + "\n"
    print(str_pos);
    ser.write(str_pos.encode('utf-8'))


ser = serial.Serial('/dev/ttyACM0', baudrate=2000000)

enviar_pos_ref(str(250), str(250))
sleep(3)

for i in range(500):
    enviar_pos_ref(str(250), str(i))
    sleep(0.05)
