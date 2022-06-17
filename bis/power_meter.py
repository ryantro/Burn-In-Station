# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 10:59:00 2022

@author: ryan.robinson

REQUIRES NI-VISA TO RUN:
    https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=PM100x
    
SCPI LANGUAGE GUIDE FOR PM101:
    https://www.thorlabs.com/_sd.cfm?fileName=MTN013681-D04.pdf&partNumber=PM101
    
    NOTE:
        THE ABREVIATED SCPI COMMANDS DONT SEEM TO WORK. USE THE COMPLETE COMMANDS
"""

import pyvisa

def main():
    """
    FOR UNIT TESTING
    """
    showResources()
    
    addr = 'USB0::0x1313::0x8076::M00808684'
    
    
    try:
        print("Trying to connect...")
        PM = PowerMeter(addr)
        print("Connected")
        PM.getIDN()
        PM.clearStatus()
        print(PM.pm.send('SYSTem:VERSion?'))
        PM.setWL(450.0)
        a = 'SENSe:CORRection:WAVelength?'
        # print(PM.pm.send(a))
        PM.getWL()
        # PM.setWL(450)
        # PM.getWL()
    finally:
        print("Closing...")
        PM.close()
    
    
    return

def showResources():
    """
    LIST AVAILIBLE USB DEVICES.
    """
    rm = pyvisa.ResourceManager()
    rm = rm.list_resources()
    print("Availible resources:")
    print(rm)
    return rm

class PowerMeter():
    def __init__(self, usbaddr = 'USB0::0x1313::0x8076::M00808684'):
        """
        CONNECT TO THORLABS PM101.
        """
        # CREATE A USB DEVICE OBJECT
        self.pm = USBDevice(usbaddr)
        
        return
    
    def getIDN(self):
        """
        GET IDN OF PM101.
        """
        # SEND IDN AND GET RESPONSE
        response = self.pm.send('*IDN?')
        
        # PRINT RESPONSE
        print(response)        
        
        # RETURN RESPONSE
        return response
    
    def clearStatus(self):
        """
        CLEAR THE STATUS OF THE DEVICE.
        """
        response = self.pm.write("*CLS")
        print(response)
        return response
    
    def setWL(self, wl = 450.0):
        """
        SET THE WAVELENGTH OF THE POWERMETER.
        """
        # SEND IDN AND GET RESPONSE
        self.pm.write('SENSe:CORRection:WAVelength {}'.format(wl))
      
        return
    
    def getWL(self):
        """
        GET THE CURRENT SET WAVELENGTH OF THE POWERMETER.
        """
        # SEND IDN AND GET RESPONSE
        response = self.pm.send('SENSe:CORRection:WAVelength?')
        
        # PRINT RESPONSE
        print(response)        
        
        # RETURN RESPONSE
        return response
    
    def getPower(self):
        """
        GET THE POWER OF THE THERMOPILE.
        """
        command = 'SENSe:CORRection:POWer'
        response = self.pm.send()
        
        print(response)
        
        return response
    
    def close(self):
        """
        CLOSE THE DEVICE.
        """
        try:
            # SHUT OFF CURRENT OUTPUT
            print("shutting off")
        finally:
            # CLOSE THE DEVICE
            self.pm.close()
        
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
    
