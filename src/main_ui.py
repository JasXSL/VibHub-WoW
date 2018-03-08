import logging, sys, signal, time, json, os, pytweening, threading
from collections import deque
from lib.vhWindows import vhWindows
from lib.vhSockets import vhSockets
from lib.vhUI import vhUI

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

class App:
    colorBuffer = bytes([0])
    # This moves
    cacheHP = 0
    conf = vhWindows()
    sock = vhSockets()
    ui = vhUI()

    # Last loop tick
    tickTime = time.time()
    # Tween value being modified
    tweenVal = 0
    # Tween start value
    tweenStart = 0
    # Time tween was started
    tweenStarted = 0
    # Local duration in case we go over max
    tweenDuration = 1

    TWEEN_DURATION = 1
    FRAMERATE = 4
    

    def __init__(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
        self.conf.onWowStatus = self.onWowRunning
        self.conf.init()
        
        self.ui.setDeviceId(self.conf.deviceID)
        self.ui.setDeviceServer(self.conf.server)
        self.ui.setCursorCoordinates(self.conf.cursor["x"], self.conf.cursor["y"])
        self.ui.onEvt = self.uiEvent

        self.sock.onConnection = self.onConnection
        self.sock.init(self.conf)

        thrd = threading.Thread(target=self.loop)
        thrd.daemon = True
        thrd.start()

        #start UI
        self.ui.begin()

    def uiEvent(self, t, data):
        c = self.conf
        if t == "settings":
            c.deviceID = data[0]
            c.server = data[1]
            c.saveConfig()
        elif t == "click":
            c.cursor["x"] = data[0]
            c.cursor["y"] = data[1]
            c.saveConfig()

    def onWowRunning(self, running):
        self.ui.setWowRunning(running)
        if not running:
            self.sock.resetVib()

    def onConnection(self, connected):
        self.ui.setConnectionStatus(connected)

    def startTween(self, amount):
        self.tweenStart = self.tweenVal+amount
        self.tweenStarted = time.time()
        if self.tweenStart < 0.25:
            self.tweenStart = 0.25
        self.tweenDuration = self.tweenStart
        dur = self.TWEEN_DURATION
        if self.tweenDuration > 4:
            self.tweenDuration = 4
        intensity = min(max(self.tweenStart*255, 0), 255)
        self.sock.sendProgram(intensity, self.tweenDuration)
        

    # Sigint handling
    def sigint_handler(self, signal, frame):
        print ('Interrupted')
        os._exit(1)
    
        
    # Threading
    def createThread(func, autostart = True):
        thrd = threading.Thread(target=func)
        thrd.daemon = True
        if autostart:
            thrd.start()
        return thrd

    def loop(self):
        while True:
            t = time.time()
            passed = t-self.tickTime
            self.tickTime = t

            self.conf.processScan()   # See if WoW is running or not
            
            if self.sock.connected and self.conf.wowPid:
                conf = self.conf
                color = conf.updatePixelColor()
                index = 0
                hpp = conf.r/255
                if hpp < self.cacheHP:
                    self.startTween((self.cacheHP-hpp)*5)
                self.cacheHP = hpp

            if self.tweenStarted:
                tweenPerc = 1-(t-self.tweenStarted)/self.tweenDuration;
                if tweenPerc < 0:
                    tweenPerc = 0
                    self.tweenStarted = 0
                elif tweenPerc > 1:
                    tweenPerc = 1
                self.tweenVal = pytweening.easeInQuad(tweenPerc)*self.tweenStart

            if not self.conf.wowPid:
                time.sleep(1)
            else:
                after = time.time()
                logicTime = 1/self.FRAMERATE-(after-t)
                if logicTime > 0:
                    time.sleep(logicTime)

#Begin
if __name__ == "__main__":
    App()
