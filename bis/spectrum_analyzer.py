# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 11:51:49 2022

@author: ryan.robinson
"""

import numpy, os
import matplotlib.pyplot as plt

# FOR OCEAN OPTICS HR4000
from seabreeze.spectrometers import Spectrometer

# CONTROLS THE OCEAN OPTICS HR4000 OSA
# REQUIRES SEABREEZE TO BE INSTALLED
class SpectrumAnalyzer():
    def __init__(self, integration_time = 2000, serialnum = "HR4D1482"):
        """
        Connect to Ocean Optics HR4000.
        Generate wavelength axis.

        Returns
        -------
        None.

        """
        
        
        # SET OSA INTEGRATION TIME
        self.integration_time = integration_time
        
        # SET OSA DEVICE
        # SERIAL NUMBER: HR4D1482
        self.spec = Spectrometer.from_serial_number(serialnum)
        
        self.spec.integration_time_micros(self.integration_time)
        
        # GET WAVELENGTH X AXIS
        self.wavelengths = self.spec.wavelengths()
        
        return
    
    def close(self):
        """
        Close the device.

        Returns
        -------
        None.

        """
        
        self.spec.close()
        
        return
    
    
    def measureSpectrum(self):
        """
        Measure data from the OSA.

        Returns
        -------
        None.

        """
        # READ INTENSITIES
        self.intensities = self.spec.intensities()
        
        return
    
    def getData(self):
        """
        Get the data in the buffer.

        Returns
        -------
        numpy array
            wavelength data.
        numpy array
            intensity data.

        """
        return self.wavelengths, self.intensities
    
    def plotSpectrum(self,title = ""):
        plt.plot(self.wavelengths,self.intensities)
        plt.xlim([435,455])
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity")
        plt.grid("On")
        plt.title(title)
        plt.pause(0.05)
        return
    
    def saveWavelengthData(self, filename):
        """
        Save the wavelength data to a csv.

        Parameters
        ----------
        filename : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Create directories for file
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save data
        numpy.savetxt(filename, self.wavelengths, delimiter = ",")
        
        return
    
    def saveIntensityData(self, filename):
        """
        Save the intensity data to a csv

        Parameters
        ----------
        filename : str
            filename and foulders to save data in.

        Returns
        -------
        None.

        """
        # Create directories for file
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Generate save data
        savedata = numpy.column_stack((self.wavelengths,self.intensities))
        
        # Save data
        numpy.savetxt(filename, savedata, delimiter = ",")
        
        return

