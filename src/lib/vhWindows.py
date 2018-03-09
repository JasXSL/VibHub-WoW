# Used for MS & Config reading/writing
# Reads from screen and harddrive
from ctypes import windll, Structure, c_long, byref
import sys, os, json, subprocess, psutil, pyperclip



class vhWindows:
    cursor = {"x":0,"y":0}
    server = "vibhub.io"
    deviceID = "TestDevice"
    appName = "VH-WoW-Python"
    dc = windll.user32.GetDC(0)
    r = 0
    g = 0
    b = 0
    wowPid = 0
    # Max intensity of output
    maxIntensity = 255
    # Percent of max intensity to add from taking damage
    hpRatio = 5

    # Event raised when WoW is started or stopped
    # Takes 1 argument which is true/false
    onWowStatus = None


    def init(self):
        argv = sys.argv
        self.getConfig()

    # Screen reader
    def updatePixelColor(self):
        parse = windll.gdi32.GetPixel(self.dc,self.cursor["x"],self.cursor["y"])
        self.r = parse & 0xFF
        self.g = (parse >> 8) & 0xFF
        self.b = (parse >> 16) & 0xFF
        #print("Parse at ", self.cursor["x"], self.cursor["y"], parse)

    # Checks if WoW is running or not
    def processScan(self):
        #Scan for WoW
        if not self.wowPid:
            cmd = 'WMIC PROCESS where "name=\'Wow-64.exe\'" get Caption,Processid'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            for line in proc.stdout:
                spl = line.split()
                if len(spl) > 1 and spl[0] == b'Wow-64.exe':
                    self.wowPid = int(spl[1])
                    if self.onWowStatus:
                        self.onWowStatus(True)

        # Make sure WoW process still exists
        elif not psutil.pid_exists(self.wowPid):
            self.wowPid = 0
            if self.onWowStatus:
                self.onWowStatus(False)

    def saveConfig(self):
        confFile = open("conf.json", "w")
        confFile.write(json.dumps({
            "cursor" : [self.cursor["x"],self.cursor["y"]],
            "server" : self.server,
            "deviceID" : self.deviceID,
            "maxIntensity" : self.maxIntensity,
            "hpRatio" : self.hpRatio
        }))
        confFile.close()

    def getConfig(self):
        try:
            confFile = open("conf.json", "r")
            js = json.loads(confFile.read())
            confFile.close()
            self.cursor["x"] = js["cursor"][0]
            self.cursor["y"] = js["cursor"][1]
            self.server = js["server"]
            self.deviceID = js["deviceID"]
            self.maxIntensity = js["maxIntensity"]
            self.hpRatio = js["hpRatio"]
            print("Loaded settings:")
            print("  DeviceID: ", self.deviceID)
            print("  Server: ", self.server)
            print("  Max Intens: ", self.maxIntensity)
            print("  HP Ratio: ", self.hpRatio)
            print("  Cursor: ", self.cursor["x"], self.cursor["y"])
            print("Start the program with reset as an argument to reconfigure")
        except FileNotFoundError:
            pass

    def copyWeakaura(self):
        try:
            confFile = open("weakaura.txt", "r")
            data = confFile.read()
            confFile.close()
            pyperclip.copy(data)
        except FileNotFoundError:
            pass
