import pyserial as ser
import platform as pltf

class servocontrol:
    
    servo = nil
    
    def __init__ (port):
        servo = serial.Serial(port, 9600, timeout=.1)
    
    def rotateservos(x, y):
        out = ('#1P' + str(x + 500)[:-2] + '#2P' + str(y+500)[:-2] + 'T100\r\n')
        servo.write(out.encode())
    
    
    
    
    
    