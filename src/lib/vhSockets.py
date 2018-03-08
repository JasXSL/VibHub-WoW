# Websocket handler
from socketIO_client_nexus import SocketIO, LoggingNamespace
import threading, json, math

class vhSockets:
    devices = []
    connected = False
    win = False
    socketIO = None

    #bindable events
    onConnection = None # bool connected
    
    def init(self, win):

        self.win = win
        print("Connecting to", win.server, LoggingNamespace)
        socketIO = SocketIO(win.server, 80)
        socketIO.on('connect', self.on_connect)
        socketIO.on('disconnect', self.on_disconnect)
        socketIO.on('reconnect', self.on_connect)
        socketIO.on('dev_online', self.on_device_connected)
        self.socketIO = socketIO

        thrd = threading.Thread(target=socketIO.wait)
        thrd.daemon = True
        thrd.start()

    #sends numbers to the socket
    def sendP( self, colorBuffer ):
        self.socketIO.emit('p', colorBuffer.hex())

    def sendProgram( self, intensity, duration ):
        easing = "Quintic.In"
        stages = [
            {"i":intensity},
            {"d":round(duration*1000), "e":easing}
            ]
        if duration >= 1.2:
            numBounces = math.floor((duration-1)/0.2)
            stages = [
                {"i":intensity},
                {"d":200, "i":0, "e":"Quintic.In", "r":numBounces},
                {"i":intensity},
                {"d":round((duration-numBounces*0.2)*1000), "e":easing}
                ]
            
        program = {
            "id" : self.win.deviceID,
            "type" : "vib",
            "data" : {
                "stages" : stages
                }
            }
        self.socketIO.emit('GET', program)
        

    def getDeviceByName(self, name):
        for i in range(0, len(self.devices)):
            if self.devices[i] == name:
                return i
        return -1

    def on_connect(self):
        self.connected = True
        win = self.win
        print('<<WS Evt>> We have connection, sending app name:', win.appName)
        self.socketIO.emit('app', win.appName, self.on_name)
        if self.onConnection:
            self.onConnection(True)

    def on_disconnect(self):
        self.connected = False
        if self.onConnection:
            self.onConnection(False)
        
        print('<<WS Evt>> on_disconnect')

    def on_hookup(*args):
        self = args[0]
        self.devices = args[1]
        print("<<WS Evt>> New devices", self.devices)

    def on_name(*args):
        self = args[0]
        print('<<WS Evt>> App name accepted, hooking up our device')
        self.setDeviceId()

    def resetDevice(self):
        self.socketIO.emit('hookdown', [], self.setDeviceId)

    def on_device_connected(*args):
        print('Device connected, resetting it')
        self = args[0]
        self.resetVib()

    def resetVib(self):
        self.sendP(bytes([0,0,0,0,0]))

    def setDeviceId(*args):
        self = args[0]
        self.socketIO.emit('hookup', self.win.deviceID, self.on_hookup)
