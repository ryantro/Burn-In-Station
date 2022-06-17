# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 17:36:57 2022

@author: ryan.robinson

Test script for the PM101 Power Meter
"""
import pyvisa

def main():
    
    showResources()
    
    
    return

def showResources():
    
    rm = pyvisa.ResourceManager()
    rm = rm.list_resources()
    
    print(rm)
    
    return

class PowerMeter():
    def __init__(self, usbaddr = "USB::4883::32842::M00466376"):
        """
        Connects to the current supply device.

        Returns
        -------
        None.

        """
        usbaddr = "USB::4883::32842::M00466376"
        
        self.itc = USBDevice(usbaddr)
        
        return
    
    def protectionQuery(self):
        """
        Tests if any protection queries are tripped.

        Returns
        -------
        test : int
            returns a value of 1 if a protection query is tripped.

        """
        vQ = "OUTPut:PROTection:VOLTage:TRIPped?"
        eQ = "OUTPut:PROTection:EXTernal:TRIPped?"
        # wQ = "OUTPut:PROTection:INTernal:TRIPped?" # Not used
        iQ = "OUTPut:PROTection:INTLock:TRIPped?"
        kQ = "OUTPut:PROTection:KEYLock:TRIPped?"
        tQ = "OUTPut:PROTection:OTEMp:TRIPped?"
        
        listQ = [vQ, eQ, iQ, kQ, tQ]
        
        test = 0
        for Q in listQ:
            response = self.itc.send(Q)
            if(response == "1"):
                print("Unable to start laser driver:\n"+Q+"\nreturned 1.")
                test = 1
        
        return test
    
    
    
    def setPulsed(self):
        """
        Switches mode to pulsed operation.

        Returns
        -------
        None.

        """
        
        command = "SOURce:FUNCtion:SHAPe PULSE"
        
        self.itc.write(command)
        
        return
    

    
    def close(self):
        """
        Closes the device.

        Returns
        -------
        None.

        """
        try:
            # SHUT OFF CURRENT OUTPUT
            self.switchOff()
        finally:
            # CLOSE THE DEVICE
            self.itc.close()
        
        return

# GENERIC USB DEVICE CLASS
# USED TO COMMUNICATE WITH THE THORLABS ITC40005    
class USBDevice:
    def __init__(self,rname):
        self.inst = pyvisa.ResourceManager().open_resource(rname)
        return None
    
    def settimeout(self,timeout):
        """
        Sets the timeout.

        Parameters
        ----------
        timeout : int
            time before an exception is thrown.

        Returns
        -------
        None.

        """
        self.inst.timeout = timeout+1000
        
        return
    
    def write(self,command):
        """
        Sends a command that requires no response. 

        Parameters
        ----------
        command : str
            command string.

        Returns
        -------
        None.

        """
        self.inst.write(command)
        
        return
    
    def send(self,command):
        """
        Sends a command that gives a response.

        Parameters
        ----------
        command : str
            command string.

        Returns
        -------
        str
            command response.

        """
        return self.inst.query(command).strip('\r\n')
    
    def close(self):
        """
        Closes the device.

        Returns
        -------
        None.

        """
        self.inst.close()
        
        return
    
    
if (__name__ == "__main__"):
    main()
    
