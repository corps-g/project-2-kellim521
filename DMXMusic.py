"""
@author: pmascal
"""

import numpy as np
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

class DMXMusic:
    
    def __init__(self, wavfilename, red_ch=2, green_ch=3, blue_ch=4, red_max=None, green_min = None, green_max = None, blue_min = None):
        """
        creates DMXMusic object
            ----------
            Parameters
            ----------
            red,green,blue_ch = channel designated (not 0 indexed)
            red,green,blue_min,max = the ranges of frequencies in each color
            red is lowest, then green, then blue. 
            
        """
        self.red_ch = red_ch
        self.green_ch = green_ch
        self.blue_ch = blue_ch
        
        self.red_max = red_max
        self.green_min = green_min
        self.green_max = green_max
        self.blue_min = blue_min
        
        # Call the functions to create all the data
        self.Spectrogram(wavfilename)
        self.AverageValues()
        self.FrameData()
        
        # If accurate rate to call this code from DMXBinary group is wanted.
        self.tStart = self.times[0]
        self.tEnd = self.times[-1]
        self.tStep = self.times[1]-self.times[0]
    
        
        
#############################################################################
    

    def Spectrogram(self, wavfilename):
        """
        Collects frequency, time, and amplitude information
        """
        
        sample_rate, samples = wavfile.read(wavfilename)
        self.frequencies, self.times, self.spectrogram = signal.spectrogram(samples, fs = sample_rate)
    
    
#############################################################################


    def AverageValues(self):
        """
        Calculate the overall average frequency for each frame
        """
        
        self.avg_vals = []
        
        for amplitudes in self.spectrogram.T:
            
            if sum(amplitudes) == 0:
                self.avg_vals.append(0)
            else:
                self.avg_vals.append(np.average(self.frequencies, weights=amplitudes))
        
#############################################################################


    def FrameData(self):
        """
        Create 2-D array that houses each frame's data.
        """
        
        # Create empty 2-D array the size that Kelli's code is expecting.
        self.frame_data = np.zeros((len(self.times),512), dtype = int)
        
        # Calculate the min and max of the audio's frequencies.
        freq_min, freq_max = int(min(self.avg_vals)), int(max(self.avg_vals))
        
        # A user is capable of giving the frequency bin parameters initially,
        # but if none were given, calculate based on range of frequencies.
        if self.red_max == None:
            self.red_max = int(freq_max/2)
        if self.green_min == None:
            self.green_min = int(self.red_max/2)
        if self.blue_min == None:
            self.blue_min = int(self.red_max)
        if self.green_max == None:
            self.green_max = int(0.5*(freq_max-self.blue_min)+self.red_max)
        
        # Set the scaled range to be from 0 to 255.
        a = 0
        b = 255
        
        # Create a scaled range of the frequencies, just for testing in the
        # matplotlib code to compare to RGB values.
        self.scaled_avg = []
        for freq in self.avg_vals:
            self.scaled_avg.append((b-a)*(freq-freq_min)/(freq_max - freq_min)+a)
        
        
        # Using the frequency bin parameters, give each frame its own
        # value for red, green, and blue, separating each value into its
        # respective element in the 2-D array (relates to channels of DMX,
        # also could be changed by user in initialization)
        for i in range(len(self.avg_vals)):
            
            red_val = (b-a)*(self.avg_vals[i]-freq_min)/(self.red_max - freq_min)+a
            green_val = (b-a)*(self.avg_vals[i]-self.green_min)/(self.green_max - self.green_min)+a
            blue_val = (b-a)*(self.avg_vals[i]-self.blue_min)/(freq_max - self.blue_min)+a
            
            if red_val > 0 and red_val < 255:
                self.frame_data[i][self.red_ch - 1] = red_val
            if green_val > 0 and green_val < 255:
                self.frame_data[i][self.green_ch-1] = green_val
            if blue_val > 0 and blue_val < 255:
                self.frame_data[i][self.blue_ch-1] = blue_val
        
    
    
#############################################################################
    

    def tcolor(self, t):
        """
        Returns a single frame's data relevant to any time given.
        """
        
        if t < self.times[0] or t > self.times[-1]:
            return 0
        else:
            return self.frame_data[np.where(self.times == self.times[self.times <= t][-1])[0][0]]
        

# Asks the user what .wav file they would like to process
def userinput():
    wavfilename = input('Name of .wav file: ')
    if wavfilename[-4:] != '.wav':
        wavfilename += '.wav'
    return wavfilename


if __name__ == "__main__":
    
    # wavfilename = 'increasing.wav'
    wavfilename = userinput()
    
    DMX = DMXMusic(wavfilename)
    
    spectrogram = DMX.spectrogram
    frequencies = DMX.frequencies
    times = DMX.times
    average_values = DMX.avg_vals
    FrameData = DMX.frame_data
    
    
    plt.plot(times, DMX.scaled_avg,'k', times, FrameData[:,DMX.red_ch-1],'r', times, FrameData[:,DMX.green_ch-1],'g', times, FrameData[:,DMX.blue_ch-1],'b')
    plt.legend(['Scaled frequency'], loc=0)
    plt.xlabel('seconds')
    plt.ylabel('0-255 scale')
    plt.show()
    
    # DMX_signal = DMX.tcolor(t)
    
    # DMX_signal[red_ch - 1] is color for red
    # DMX_signal[green_ch - 1] is color for green
    # DMX_signal[blue_ch - 1] is color for blue