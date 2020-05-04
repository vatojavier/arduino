import serial
ser = serial.Serial('/dev/ttyACM0')

string = "hola"
numero = 10

while 1:
    print("Mete: ")
    numero = input()
    #numero = ((numero/))
    #ser.write(numero.to_bytes(1, 'big', signed=False))
    ser.write(numero.encode('utf-8'))