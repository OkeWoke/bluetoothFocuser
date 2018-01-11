import bluetooth
import Tkinter as tki
import threading

        
class TS:
    def __init__(self):
        """Creating the initial bluetooth connection and defining the char protocol"""
        print("Checking connection...")
        self.serverMACAddress = '20:15:10:12:39:01'
        self.port = 1
        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.s.connect((self.serverMACAddress, self.port))
        self.CW = ["A","B","C","D"]
        self.CCW = ["Z","Y","X","W"]
        self.speed = 0#Default at 25%
        #Maps speeds 0 to 3, 0 being 25%, 3 being 100%
        self.threads =[]

    def reconnect(self):
        """Handles the reconnection to the bluetooth module"""
        #self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        if len(self.threads) >=1:
            del self.threads[0:]
        try:
            self.s.close()
        except Exception as e:
            print("Failed to close socket")
            print(e)
        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.s.connect((self.serverMACAddress, self.port))
        
    def _deco(func):
        """Decorator function that handles errors"""
        def blah(self,*arg):
            try:
                func(self,*arg)
            except IOError:
                print("Bluetooth Error")
                self.reconnect()
                
        return blah
    
    @_deco
    def handshake(self):
        """Handshaking between the arduino to check the connection is valid"""
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
        """Closes the connection and kills the program"""
        print("closing connection...")
        self.s.close()
        quit()
    
    def change_Focus(self, rate):
        """Changes the speed of the focuser"""
        self.speed = int(rate)
        print("Setting Focus Rate to: " + str(rate))
    
    @_deco
    def focus_Halt(self,e):
        """sends the H command to the arduino, halting the focuser, additionally has handshake verification"""
        a = threading.Thread(target=self.handshake)
        self.threads.append(a)
        a.start()
        print("\nHalting focuser\n")
        self.s.send("H")
        
    @_deco
    def focus_Left(self,e):
        print("sending "+self.CCW[self.speed])
        self.s.send(self.CCW[self.speed])
        
    @_deco
    def focus_Right(self,e):
        print("sending "+self.CW[self.speed])
        self.s.send(self.CW[self.speed])


class App(TS):

    WINDOW_TITLE = "Telescope Control Software"
    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 300
    SLEW_OPTIONS = ["0","1","2","3"]
    
    def __init__(self,root_win,ts):
        """Setting up the frames and windows"""
        self.ts = ts

        root_win.title(self.WINDOW_TITLE)
        root_win.minsize(self.WINDOW_WIDTH,self.WINDOW_HEIGHT)
        #root_win.protocol("WM_DELETE_WINDOW", self.ts.closeConnection)
        

        self.control = tki.Frame(root_win)
        self.controlFrame()
        self.control.config(height=self.WINDOW_HEIGHT,width=600,borderwidth=2,relief="groove")
        self.control.grid(row=0,column =1,sticky="N")

        self.checkConnection()
    
    def controlFrame(self):
        """Widgets for Telescope Control Frame"""

        #Focus Buttons
        focusVar = tki.StringVar(self.control)
        slewRevOpt = list(self.SLEW_OPTIONS)
        
        focus_OptionMenu = tki.OptionMenu(self.control,focusVar,*self.SLEW_OPTIONS,command= lambda x: self.ts.change_Focus(slewRevOpt.index(focusVar.get()))) 
        self.left_button = tki.Button(self.control,text="<")
        self.right_button = tki.Button(self.control, text=">")
        
        
        self.left_button.bind('<ButtonPress-1>',self.ts.focus_Left)
        self.left_button.bind('<ButtonRelease-1>',self.ts.focus_Halt)
        self.right_button.bind('<ButtonPress-1>',self.ts.focus_Right)
        self.right_button.bind('<ButtonRelease-1>',self.ts.focus_Halt)
        
        
        #Labels and placement
        tki.Label(self.control,text="Telescope Control").grid(column=0, row=0,columnspan=4,ipadx=50)    
        tki.Label(self.control, text="Focus Control").grid(column=0,columnspan=4,row=4)
        tki.Label(self.control,text="Focus Speed").grid(column=0,columnspan=2,row=5)
        
        focus_OptionMenu.grid(column=2,columnspan=2,row=5)
        
        self.left_button.grid(column=0,columnspan=2,row=6)
        self.right_button.grid(column=2,columnspan=2,row=6)
       
    def checkConnection(self):
        """Handle GUI depending on connection status"""
        if len(self.ts.threads) >2:
            self.left_button.config(state = 'disabled')
            self.right_button.confg(state = "disabled")
        else:
            self.left_button.config(state = 'normal')
            self.right_button.config(state = 'normal')
        
        self.left_button.update()
        self.right_button.update()
        root.after(100,self.checkConnection)
        
        
if __name__ =="__main__":
    root = tki.Tk()
    app = App(root,TS())
    root.mainloop()
#note checkConnection will re enable the buttons when the reconnect function deletes all the threads, need to deal with the reconnect function thread handling and reconnection.
