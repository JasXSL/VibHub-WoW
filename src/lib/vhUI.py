import tkinter as tk, threading
from tkinter import messagebox

class vhUI:
    root = None
    connectionStatus = None
    targetCoordinates = None
    inputDeviceID = None
    inputServer = None
    targetButton = None
    settingsButton = None
    onEvt = None
    wowRunning = None
    
    def __init__(self):
        root = tk.Tk()
        root.title("WoW VibHub Connector")
        self.root = root
        self.root.grid_columnconfigure(0, weight=1)
        icon = tk.PhotoImage(file = r'icon.png')
        root.tk.call('wm', 'iconphoto', root._w, icon)
        # Connection status
        row = 0
        self.wowRunning = tk.Label(
            self.root,
            padx = 10,
            pady = 5,
            fg = "dark red",
            font = "helvetica 12 bold",
            text = "WoW Not Running"
            )
        self.wowRunning.grid(row=row, columnspan=2)

        # Connection status
        row = row+1
        self.connectionStatus = tk.Label(
            self.root,
            padx = 10,
            pady = 5,
            fg = "dark red",
            text = "Disconnected"
            )
        self.connectionStatus.grid(row=row, columnspan=2)

        # Coordinates
        row = row+1
        self.targetCoordinates = tk.Label(
            self.root,
            padx = 10,
            pady = 5,
            text = "Tracking X: 0 Y: 0"
            )
        self.targetCoordinates.grid(row=row, columnspan=2)

        # TargetButton
        row = row+1
        self.targetButton = tk.Button(
            self.root,
            text='Pick Target',
            font = "helvetica 12 bold",
            width=25,
            command=self.onTargetButton
            )
        self.targetButton.grid(row=row, columnspan=2)

        # HR
        row = row+1
        canvas = tk.Canvas(self.root, width=250, height=5)
        canvas.create_line(0,5,250,5,width=1,dash=1)
        canvas.grid(row=row, columnspan=2)

        # DeviceID insert
        row = row+1
        tk.Label(
            self.root,
            text = "DeviceID:",
            font = "helvetica 12",
            anchor = "w",
            width=8
            ).grid(row=row, sticky="w")
        self.inputDeviceID = tk.Text(
            self.root,
            height=1,
            font = "helvetica 12",
            width=20,
            )
        self.inputDeviceID.grid(row=row, column=1)
        self.inputDeviceID.insert(tk.END, "BigRedButton")

        # Server insert
        row = row+1
        tk.Label(
            self.root,
            text = "Server:",
            font = "helvetica 12",
            anchor = "w",
            width=8
            ).grid(row=row, sticky="w")
        self.inputServer = tk.Text(
            self.root,
            height=1,
            font = "helvetica 12",
            width=20,
            )
        self.inputServer.grid(row=row, column=1)
        self.inputServer.insert(tk.END, "vibhub.io")


        #Save button
        row = row+1
        self.settingsButton = tk.Button(
            self.root,
            text='Save',
            width=25,
            font = "helvetica 12",
            command=self.onSettingsSave
            )
        self.settingsButton.grid(row=row, columnspan=2, sticky='we')

    def begin(self):
        self.root.mainloop()
        
    def onTargetButton(self):
        tk.messagebox.showinfo("Recording", "Click the weakaura on your screen. Hit escape to cancel.")
        vhOverlay(self.onOverlayClick)

    def onSettingsSave(self):
        devid = self.inputDeviceID.get("1.0",tk.END).strip()
        serv = self.inputServer.get("1.0",tk.END).strip()
        self.raiseEvent("settings", [devid, serv])
        tk.messagebox.showinfo("Settings Saved!", "Settings have been saved!")

    def setDeviceId(self, deviceid):
        t = self.inputDeviceID
        t.delete("1.0", tk.END)
        t.insert(tk.END, deviceid)

    def setDeviceServer(self, server):
        t = self.inputServer
        t.delete("1.0", tk.END)
        t.insert(tk.END, server)

    def setCursorCoordinates(self, x, y):
        tx = "Tracking X: "+ str(x) +" Y: "+ str(y) 
        self.targetCoordinates.config(text=tx)
    
    def raiseEvent(self, evtype, data):
        if self.onEvt:
            self.onEvt(evtype, data)

    def onOverlayClick(self, coordinates):
        self.raiseEvent("click", coordinates)

    def setConnectionStatus(self, connected):
        self.connectionStatus.config(
            fg="dark green" if connected else "dark red",
            text="Connected" if connected else "Disconnected"
            )
        
    def setWowRunning(self, running):
        self.wowRunning.config(
            fg="dark green" if running else "dark red",
            text="WoW Is Running" if running else "WoW Not Running"
            )
    

# Overlay
class vhOverlay:
    root = None
    callback = None
    
    def __init__(self, callback):
        root = tk.Toplevel()
        root.title = "Click the weakaura"
        root.attributes("-alpha", 0.1)
        root.attributes("-topmost")
        root.configure(background="black")
        root.state('zoomed')
        root.overrideredirect(1)
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        self.callback = callback
        self.root = root       
        root.bind("<Escape>", self.close)
        root.bind("<Button-1>", self.onClick)
        root.focus_force() # <-- move focus to this widget
        root.mainloop()

    def onClick(self, event):
        if self.callback:
            self.callback([event.x, event.y])
        self.close(None)

    def close(self, event):
        self.root.destroy()



