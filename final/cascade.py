import platform

def cascadedir():
    if platform.uname().system == 'Linux':
        return '/home/cavej376/kek/final/haarcascade_frontalface_default.xml'
    else:
        return 'haarcascade_frontalface_default.xml'