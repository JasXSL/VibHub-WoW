import logging, sys, signal, threading, time as mainTime, json, os
from socketIO_client_nexus import SocketIO, LoggingNamespace
from ctypes import windll, Structure, c_long, byref
from pynput.keyboard import Key, Controller
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
from collections import deque

# Used for MS
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

# Sigint handling
def sigint_handler(signal, frame):
    print ('Interrupted')
    os._exit(1)
signal.signal(signal.SIGINT, sigint_handler)


# Globals
devices = []
connected = False
cursor = POINT()
dc= windll.user32.GetDC(0)
colorBuffer = bytes([0])
APP_NAME = "WowTest"
DEVICE_NAME = "BigRedButton"
keyboard = Controller()
bSound = pygame.mixer.Sound("big_button_press.wav")
aSound = pygame.mixer.Sound("alarm_proper.wav")
aSound.set_volume(0.4)
CACHE_HP = 0
always_intro = pygame.mixer.Sound("always_intro.wav")
always_loop = pygame.mixer.Sound("always_loop.wav")
always_intro.set_volume(0.4)
always_loop.set_volume(0.4)
cache_flags = 0

# Generic
def createThread(func, autostart = True):
    thrd = threading.Thread(target=func)
    thrd.daemon = True
    if autostart:
        thrd.start()
    return thrd



# Screen reader
def getPixelColor(x, y):
    parse = windll.gdi32.GetPixel(dc,x,y)
    return [parse & 255,(parse >> 8) & 255,(parse >> 16) & 255]

def getCursorPosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt

def getConfig():
    try:
        confFile = open("conf.json", "r")
        js = json.loads(confFile.read())
        confFile.close()
        cursor.x = js[0]
        cursor.y = js[1]
        print(cursor.x, cursor.y)
        return True
    except FileNotFoundError:
        return False


# VibHub
#sends numbers to the socket
def sendNumbers():
    global colorBuffer
    socketIO.emit('p', colorBuffer.hex())

def getDeviceByName(name):
    global devices
    for i in range(0, len(devices)):
        if devices[i] == name:
            return i
    return -1

def on_connect():
    global connected, APP_NAME
    connected = True
    print('<<WS Evt>> We have connection, sending app name')
    socketIO.emit('app', APP_NAME, on_name)

def on_disconnect():
    global connected
    connected = False
    print('<<WS Evt>> on_disconnect')

def on_hookup(*args):
    global devices, socketIO
    devices = args[0]
    print("<<WS Evt>> New devices", devices)
    

def on_name(*args):
    global socketIO, DEVICE_NAME
    print('<<WS Evt>> App name accepted, hooking up our device')
    socketIO.emit('hookup', DEVICE_NAME, on_hookup)

def on_device_connected(*args):
    print('Device connected')
    sendNumbers()

def on_custom(*args):
    global keyboard, bSound
    #print('<<WS Evt>> Got custom data:', args, len(args))
    data = args[0]
    deviceid = data[0]
    socketid = data[1]
    data = data[2]
    if not isinstance(data, list):
        return
    data = deque(data)
    task = data.popleft()
    val = data.popleft()
    if task == "btn" and not val:
        bSound.play()
        print("Playing sound!")
        keyboard.press('0')
        keyboard.release('0')
        
        
    

# Begin program
print("Loading config")
logger.info('Initializing')
if __name__ == "__main__":
    argv = sys.argv
    refresh = True
    if len(argv) < 2 or argv[1] != "reset":
        refresh = not getConfig()
    if refresh:
        input("Hover over the box and hit enter to start!")
        cursor = getCursorPosition()
        confFile = open("conf.json", "w")
        confFile.write(json.dumps([cursor.x,cursor.y]))
        confFile.close()
    print("Init completed")

#start socketiO
print("Starting websockets")
logger.info("Starting socket.io")
socketIO = SocketIO('vibhub.io', 80, LoggingNamespace)
socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_connect)
socketIO.on('aCustom', on_custom)
socketIO.on('dev_online', on_device_connected)
createThread(socketIO.wait)


def quadrify(n):
    if n >= 255:
        return 255
    return round(pow(n/255, 3)*0.6*255)

print("Starting main program")
logger.info("Starting Program loops")
# Main program loop
def programLoop():
    global connected, cursor, colorBuffer, CACHE_HP, aSound, cache_flags
    while True:
        mainTime.sleep(1/30)

        if connected:
            color = getPixelColor(cursor.x, cursor.y)
            index = 0
            buffer = bytes([
                index,
                color[0],
                color[1],
                color[2]
            ])
            hpp = color[0]/255
            
            if (hpp < 0.35) != (CACHE_HP < 0.35):
                if hpp < 0.35:
                    aSound.play(-1)
                else:
                    aSound.fadeout(500)
                    
            if hpp <= 0 and CACHE_HP > 0:
                aSound.fadeout(500)
                
            CACHE_HP = hpp
            
            if buffer != colorBuffer:
                colorBuffer = buffer
                sendNumbers()
                
            flags = color[2]

            if (flags&2) != (cache_flags&2):
                print(flags)
                if flags&2:
                    print("Playing INTRO")
                    always_intro.play()
                    pygame.time.set_timer(pygame.USEREVENT, 950)
                else:
                    print("Stopping intro!")
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    always_loop.fadeout(500)
                    
            cache_flags = flags

            
        for e in pygame.event.get():
            if e.type == pygame.USEREVENT: 
                always_loop.play(-1)
                pygame.time.set_timer(pygame.USEREVENT, 0)
                
            if e.type == pygame.QUIT: break

#createThread(programLoop)
programLoop()
