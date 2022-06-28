# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 16:21:28 2022

@author: ryan.robinson
"""

import tkinter as tk
from functools import partial
import time, datetime
import threading

class Application:
    def __init__(self, master):
        """
        CREATE THE PROGRAM GUI
        """
        self.master = master
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # BOX CONFIGURE
        self.master.title('BIS - Burn In Station')
        
        # DEFINE RUNFRAME
        self.runframe = tk.Frame(self.master)
        self.runframe.rowconfigure([0, 1, 2, 3, 4, 5], minsize=30, weight=1)
        self.runframe.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8], minsize=25, weight=1)
        
        # DEFINE ROW LABELS
        self.rowLabels = []
        for i in range(1,5):
            self.rowLabels.append(tk.Label(self.runframe, text = "ROW {}".format(i), font = ('Ariel 15')))
            self.rowLabels[-1].grid(row = i, column = 0, sticky = "NSWE", padx = 5, pady = 5)
        
        # DEFINE COLUMN LABELS
        colLabels = []
        for i in range(1,8):
            colLabels.append(tk.Label(self.runframe, text = "COLUMN {}".format(i), font = ('Ariel 15')))
            colLabels[-1].grid(row = 0, column = i, sticky = "NSWE", padx = 5, pady = 5)
        buttonLabel = tk.Label(self.runframe, text = "BUTTON", font = ('Ariel 15'))
        buttonLabel.grid(row = 0, column = 8, sticky = "NSWE", padx = 5, pady = 5)
        
        """ DEFINE HEXEL BOXES """
        self.hexels = []
        for i in range(1,5):
            for j in range(1,8):
                # GENERATE HEXEL NUMBER ENTRY BOX
                self.hexels.append(HexelBox(self.runframe, i = "({},{})".format(i,j)))
                self.hexels[-1].box.grid(row = i, column = j, padx = 1, pady = 1)

        # DEFINE TOGGLE BUTTONS
        self.on = tk.PhotoImage(file = r"images/on.png")
        self.off = tk.PhotoImage(file = r"images/off.png")
        self.toggleButtons = []
        self.buttonStates = []
        for i in range(0,4):
            self.buttonStates.append(False)
            test = partial(self.switch, i)
            self.toggleButtons.append(tk.Button(self.runframe, text = "test{}".format(i), image = self.off, bd = 0, command = test))
            self.toggleButtons[-1].grid(row = i+1, column = 8, sticky = "NSWE", padx = 5, pady = 5)

        
        # PACK THE GUI
        self.runframe.pack()
        
        # RUNNING
        self.running = True
        
        # CREATE THREAD OBJECT FOR TIME KEEPING
        self.timeTrackingThread = threading.Thread(target = self.timeTracking)
        
        # START THREAD
        self.timeTrackingThread.start()
        
        # CREATE THREAD OBJECTING FOR MEASUREMENT
        self.measurementThread = None
        
        """
        TODO
            ADD TARGET TO MEASUREMENT THREAD
            START MEASUREMENT THREAD
        """
        
        return

    def timeTracking(self):
        """
        RECORD THE RUNNING TIME OF A ROW OF HEXELS
        """
        while(self.running):
            
            for hexel in self.hexels:
                if(hexel.running):
                    hexel.updateTime()
            
            time.sleep(0.1)
        
        return

    def switch(self,i):
        """
        TOGGLE BUTTON FOR TURNING ON/OFF ROWS OF HEXELS
        """
        # SWITCH BUTTON OFF
        if(self.buttonStates[i]):
            self.toggleButtons[i].config(image = self.off)
            self.buttonStates[i] = False
 
            for j in range(0,7):
                self.hexels[j + (i * 7)].unlock()
        
        # SWITCH BUTTON ON
        else:
            self.toggleButtons[i].config(image = self.on)
            self.buttonStates[i] = True

            for j in range(0,7):
                self.hexels[j + (i *7)].lock()
        
        return

    def on_closing(self):
        """
        EXIT THE APPLICATION
        """
        # PROMPT DIALOG BOX
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            
            # MARK RUNNING FLAG AS FALSE
            self.running = False
            
            # JOIN TIME TRACKING THREAD
            self.timeTrackingThread.join()
            
            """
            TODO
                JOIN MEASUREMENT THREAD
            """
            
            # DESTROY APPLICATION
            self.master.destroy()
            
        return

    def measurementLoop(self):
        """
        LOOP THAT HANDLES TAKING MEASUREMENTS
        """
        # TIME LAST MEASUREMENT WAS TAKEN AT
        tLast = time.time()
        
        # DESIGNATED TIME BETWEEN MEASUREMENTS
        tDelta = 600.0 # SECONDS
        
        while(self.running):
            
            for hexel in self.hexels:
            
                # CHECK IF IT IS TIME FOR A MEASUREMENT
                if(tDelta < (time.time() - tLast) or hexel.firstTime):
                    """
                    TODO
                        1. MOVE STAGE TO HEXEL POSITION
                            - STORE HEXEL POSITION IN HEXEL BOX OBJECT?
                            - STAGE.MOVE(HEXEL.X,HEXEL.Y)
                        2. TAKE POWER AND SPECTRUM
                        3. UPDATE HEXEL OBJECT
                    """
                    
                    
                    # MARK FIRST TIME AS FALSE
                    self.firstTime = False
                        
                    # RESET MEASUREMENT TIMER
                    tLast = time.time()
            
            """
            TODO
                RETURN STAGES TO HOME POSITIONS
            """
            
            # SLEEP 5 SECONDS
            time.sleep(5)
            
        return
        

class HexelBox:
    def __init__(self, master, i = "0"):
        """
        FRAME FOR INDIVIDUAL HEXEL BOX.
        ________________
        | MODULE #     |
        |______________|
        | HEXEL SERIAL |
        |______________|
        |        POWER |
        |______________|
        |           WL |
        |______________|
        """
        # DEFINE HEXEL SERIAL NUMBER
        # self.hexel = '100----'
        
        # DEFINE FRAME
        self.box = tk.Frame(master, highlightbackground="black", highlightthickness=1)
        self.box.rowconfigure([0, 1, 2, 3, 4], minsize=2, weight=1)
        
        # DEFINE FRAME LABEL
        self.boxLabel = tk.Label(self.box, text = "MODULE {}".format(i), font = ('Ariel 8'))
        self.boxLabel.grid(row=0, sticky = "NSW", padx = 5, pady = 0)
        
        # SETUP HEXEL ENTRY BOX
        self.hexel = tk.StringVar(self.box, value = "100----")
        self.hexelBox = tk.Entry(self.box, width = 8, textvariable = self.hexel, font = ('Ariel 17'), borderwidth = 2, bg = '#84e47e')
        self.hexelBox.config(disabledbackground = '#F55e65')
        self.hexelBox.grid(row=1, sticky = "NSWE", padx = 5, pady = 0)
        
        # SETUP POWER VARIABLE AND LABEL
        self.pw = tk.StringVar(self.box, value = '-.- W')
        self.pwLabel = tk.Label(self.box, textvariable = self.pw, font = ('Ariel 8'))
        self.pwLabel.grid(row=2, sticky = "NSE", padx = 5, pady = 0)
        
        # SETUP WAVELENGTH VARIABLE AND LABEL
        self.wl = tk.StringVar(self.box, value = '-.- nm')
        self.wlLabel = tk.Label(self.box, textvariable = self.wl, font = ('Ariel 8'))
        self.wlLabel.grid(row=3, sticky = "NSE", padx = 5, pady = 0)
                
        # SETUP TIMER AND LABEL
        self.t = tk.StringVar(self.box, value = '-.- s')
        self.tLabel = tk.Label(self.box, textvariable = self.t, font = ('Ariel 8'))
        self.tLabel.grid(row=4, sticky = "NSE", padx = 5, pady = 0)     
        
        # BOX VARIABLES
        self.running = False # False for off, True for on
        self.startTime = 0.0
        self.tCum = 0.0
        self.hexel_old = self.hexel.get()
        self.firstTime = True # True for first measurement, false for subsequent measurements
        self.coords = [0.0, 0.0] # HEXEL MODULE X AND Y POSITIONS
        return
    
    def lock(self):
        """
        LOCK THE BUTTON TO PREVENT WRITING A NEW SERIAL NUMBER.
        """
        # DISABLE ENTRY BOX
        self.hexelBox.config(state = "disabled")
        
        # MARK THAT HEXEL IS RUNNING
        self.running = True
        
        # RECORD START TIME OF PROGRAM
        self.startTime = time.time()
        
        # CHECK IF HEXEL IS NEW HEXEL
        if(self.hexel_old != self.hexel.get()):
            self.hexel_old = self.hexel.get()
            self.tCum = 0.0
            self.pw.set('-.- W')
            self.wl.set('-.- nm')
            
        return
    
    def unlock(self):
        """
        UNLOCK BUTTON TO ALLOW WRITING HEXEL SERIAL NUMBER.
        """
        # ENABLE ENTRY BOX
        self.hexelBox.config(state = "normal")
        
        # INDICATE THAT 
        self.running = False
        
        # RECORD RUN TIME
        self.tCum = time.time() - self.startTime + self.tCum
        
        return

    def updateTime(self):
        """
        UPDATE THE RUN TIME OF THE APPLICATION.
        """
        # FIND RUN TIME IN SECONDS
        tSeconds = time.time() - self.startTime + self.tCum
        
        # CONVERT RUN TIME TO HR:MIN:SEC FORMAT
        tDateTime = "{}".format(datetime.timedelta(seconds = tSeconds)).split(".")[0]
        
        # WRITE TIME TO TKINTER VARIABLE
        self.t.set(tDateTime)
        
        return

    def getHexelSerial(self):
        """
        GET THE SERIAL NUMBER OF A HEXEL.
        """      
        
        return self.hexel.get()

class DataMeasurement:
    def __init__(self):
        
        
        
        return
    
    def MeasurementLoop(self):
        return


def main():
    # CREATE ROOT TKINTER OBJECT
    root = tk.Tk()
    
    # CREATE APPLICATION
    app = Application(root)
    
    # RUN MAINLOOP
    root.mainloop()
    
    return
    
if __name__=="__main__":
    main()


