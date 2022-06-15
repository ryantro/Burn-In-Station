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
        
        self.master = master
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # BOX CONFIGURE
        self.master.title('BIS - Burn In Station')
        
        # DEFINE RUNFRAME
        self.runframe = tk.Frame(self.master)
        self.runframe.rowconfigure([0, 1, 2, 3, 4, 5], minsize=30, weight=1)
        self.runframe.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], minsize=25, weight=1)
        
        # DEFINE ROW LABELS
        s = 1
        e = 5
        self.rowLabels = []
        for i in range(s,e):
            self.rowLabels.append(tk.Label(self.runframe, text = "ROW {}".format(4-i), font = ('Ariel 15')))
            self.rowLabels[-1].grid(row = i, column = 0, sticky = "NSWE", padx = 5, pady = 5)
        
        # DEFINE COLUMN LABELS
        colLabels = []
        for i in range(1,8):
            colLabels.append(tk.Label(self.runframe, text = "COLUMN {}".format(i), font = ('Ariel 15')))
            colLabels[-1].grid(row = 0, column = i, sticky = "NSWE", padx = 5, pady = 5)
        buttonLabel = tk.Label(self.runframe, text = "BUTTON", font = ('Ariel 15'))
        buttonLabel.grid(row = 0, column = 8, sticky = "NSWE", padx = 5, pady = 5)
        runTimeLabel = tk.Label(self.runframe, text = "RUNTIME", font = ('Ariel 15'))
        runTimeLabel.grid(row = 0, column = 9, sticky = "NSWE", padx = 5, pady = 5)
        
        # DEFINE HEXEL ENTRY BOXES
        self.hexels = []
        for i in range(s,e):
            for j in range(1,8):
                # GENERATE HEXEL NUMBER ENTRY BOX
                self.hexels.append(tk.Entry(self.runframe, text = 'hexel{}{}'.format(i,j), width = 8, font = ('Ariel 17'), borderwidth = 2, bg = '#84e47e'))
                self.hexels[-1].insert(0, '100XXXX')
                self.hexels[-1].grid(row=i, column=j, sticky = "NSWE", padx = 5, pady = 5)

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


        # DEFINE RUNTIME COUNTERS
        self.timeLabels = []
        self.time = []
        for i in range(0,4):
            self.time.append(tk.StringVar())
            self.time[-1].set("0.0")
            self.timeLabels.append(tk.Label(self.runframe, textvariable = self.time[-1], font = ('Ariel 15')))
            self.timeLabels[-1].grid(row=i+1, column=9, sticky = "NSWE", padx = 5, pady = 5)
            
        self.runframe.pack()
        
        # RUNNING
        self.running = True
        
        # CREATE THREAD OBJECT TARGETTING THE PROGRAM
        self.thread1 = threading.Thread(target = self.runTime)
        
        # START THREAD
        self.thread1.start()
        
        return

    def runTime(self):
        self.startTime = [time.time(), time.time(), time.time(), time.time()]
        while(self.running):
            for i in range(0,4):
                if(self.buttonStates[i]):
                    t = "{}".format(datetime.timedelta(seconds = time.time() - self.startTime[i])).split(".")[0]
                    self.time[i].set("{}".format(t))
            
            time.sleep(0.1)
        
        return

    def switch(self,i):
        
        if(self.buttonStates[i]):
            self.toggleButtons[i].config(image = self.off)
            self.buttonStates[i] = False
            self.startTime[i] = time.time()
        
        else:
            self.toggleButtons[i].config(image = self.on)
            self.buttonStates[i] = True
            self.startTime[i] = time.time()
        
        return

    def on_closing(self):
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.running = False
            self.thread1.join()
            self.master.destroy()
            
        return

class HexelBox:
    def __init__(self, master):
        """
        FRAME FOR INDIVIDUAL HEXEL BOX
        ________________
        | HEXEL SERIAL |
        |______________|
        | HEXEL POWER  |
        |______________|
        | HEXEL WL     |
        |______________|
        
        Parameters
        ----------
        master : Tkinter Frame
       
        Returns
        -------
        None.

        """
        # DEFINE FRAME
        self.box = tk.Frame(master)
        self.box.rowconfigure([0, 1, 2], minsize=30, weight=1)
        
        # SETUP HEXEL ENTRY BOX
        self.hexel = tk.Entry(self.box, width = 8, font = ('Ariel 17'), borderwidth = 2, bg = '#84e47e')
        self.hexel.insert(0, '100XXXX')
        self.hexel.grid(row=0, sticky = "NSWE", padx = 5, pady = 5)
        
        # SETUP POWER VARIABLE AND LABEL
        self.pw = tk.StringVar()
        self.pw.set("0.0 W")
        self.pwLabel = tk.Label(self.box, textvariable = self.pw, font = ('Ariel 8'))
        self.pwLabel.grid(row=1, sticky = "NSWE")
        
        # SETUP WAVELENGTH VARIABLE AND LABEL
        self.wl = tk.StringVar()
        self.wl.set("0.0 nm")
        self.wlLabel = tk.Label(self.box, textvariable = self.wl, font = ('Ariel 8'))
        self.wlLabel.grid(row=2, sticky = "NSWE")
                        
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


