import bluetooth
import Tkinter as tki
import threading
"""
def error_decorator(re):
    def wrapper(f):
        try:
            print("in dec")
            return f
        except IOError:
            print("Bluetooth Error")
            re(self=None)
    return wrapper
"""

class error_decorator:
    def __init__(self,re):
        self.re = re
    
    def __call__(self,func,*args,**kwargs):
        def deco(*args,**kwargs):
            try:
                print(args)
                print(kwargs)
                return func(args,kwargs)
            except IOError:
                print("Connection error, reconnecting...")
                return self.re
        return deco(args,kwargs)
        
class TS:
    def __init__(self):
        print("Checking connection...")
        self.serverMACAddress = '20:15:10:12:39:01'
        self.port = 1
        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.s.connect((self.serverMACAddress, self.port))
        self.CW = ["A","B","C","D"]
        self.CCW = ["Z","Y","X","W"]
        self.speed = 0#Default at 25%
        #Maps speeds 0 -3, 0 being 25%, 3 being 100%
        self.threads =[]

    def reconnect(self):
        #self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        try:
            self.s.close()
        except Exception as e:
            print("Failed to close socket")
            print(e)
        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.s.connect((self.serverMACAddress, self.port))
        
    def _deco(func):
        def blah(self,*arg):
            try:
                func(self,*arg)
            except IOError:
                print("Bluetooth Error")
                self.reconnect()
                
        return blah
    
    @_deco
    def handshake(self):
        print("No: "+str(len(self.threads)))
        indexes_to_del = []
        if len(self.threads)>3:
                    raise IOError
        for i in range(0,len(self.threads)):
            if not self.threads[i].is_alive():
                indexes_to_del.append(i)
                
        for i in indexes_to_del:#do this otherwise if deleted above, out of index error occurs
            del self.threads[i]
        
        while True:
            data =  self.s.recv(1024)
            if data =="O":
                print("Hanshake Received")
                return
        

    def closeConnection(self):
        print("closing connection...")
        self.s.close()
        quit()
    
    def change_Focus(self, rate):
        self.speed = int(rate)
        print("Setting Focus Rate to: " + str(rate))
    
    @_deco#@error_decorator(reconnect)
    def focus_Halt(self,e):
        a = threading.Thread(target=self.handshake)
        self.threads.append(a)
        a.start()
        print("\nHalting focuser\n")
        self.s.send("H")
        #print(str(self.s.recv(1024)))
        
        
    @_deco#@error_decorator(reconnect)
    def focus_Left(self,e):
        print("sending "+self.CCW[self.speed])
        self.s.send(self.CCW[self.speed])
        
    @_deco#@error_decorator(reconnect)
    def focus_Right(self,e):
        print("sending "+self.CW[self.speed])
        self.s.send(self.CW[self.speed])
        
class App(TS):

    WINDOW_TITLE = "Telescope Control Software"
    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 300
    SLEW_OPTIONS = ["0","1","2","3"]
    
    def __init__(self,root_win,ts):
        self.ts = ts

        root_win.title(self.WINDOW_TITLE)
        root_win.minsize(self.WINDOW_WIDTH,self.WINDOW_HEIGHT)
        #root_win.protocol("WM_DELETE_WINDOW", self.ts.closeConnection)
        

        self.control = tki.Frame(root_win)
        self.controlFrame()
        self.control.config(height=self.WINDOW_HEIGHT,width=600,borderwidth=2,relief="groove")
        self.control.grid(row=0,column =1,sticky="N")
    
    def controlFrame(self):
        """Widgets for Telescope Control Frame"""

        #Focus Buttons
        focusVar = tki.StringVar(self.control)
        slewRevOpt = list(self.SLEW_OPTIONS)
        #slewRevOpt.reverse()
        focus_OptionMenu = tki.OptionMenu(self.control,focusVar,*self.SLEW_OPTIONS,command= lambda x: self.ts.change_Focus(slewRevOpt.index(focusVar.get()))) 
        left_button = tki.Button(self.control,text="<")
        right_button = tki.Button(self.control, text=">")
        #connect_button = tki.Button(self.control,text="Reconnect")
        
        left_button.bind('<ButtonPress-1>',self.ts.focus_Left)
        left_button.bind('<ButtonRelease-1>',self.ts.focus_Halt)
        right_button.bind('<ButtonPress-1>',self.ts.focus_Right)
        right_button.bind('<ButtonRelease-1>',self.ts.focus_Halt)
        #connect_button.bind('<ButtonPress-1>', self.ts.reconnect)
        
        #Labels and placement
        tki.Label(self.control,text="Telescope Control").grid(column=0, row=0,columnspan=4,ipadx=50)    
        tki.Label(self.control, text="Focus Control").grid(column=0,columnspan=4,row=4)
        tki.Label(self.control,text="Focus Speed").grid(column=0,columnspan=2,row=5)
        
        focus_OptionMenu.grid(column=2,columnspan=2,row=5)
        
        left_button.grid(column=0,columnspan=2,row=6)
        right_button.grid(column=2,columnspan=2,row=6)
        #connect_button.grid(column=0,columnspan=4,row=7)

root = tki.Tk()
app = App(root,TS())
root.mainloop()
