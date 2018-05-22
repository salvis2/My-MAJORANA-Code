import numpy as np
import matplotlib.pyplot as plt
import math
import scipy
from scipy.fftpack import rfft, irfft, fftfreq
#import excel sheet
#keep time and post-amplifier voltage
#zeroth column  is time, all other columns are voltages
input_data = np.genfromtxt(r"C:\Users\sebas\OneDrive\Documents\Yang\PulseHeights.txt") #, delimiter = ",")
num_pulses = len(input_data[0]) - 1
pulse_heights = np.zeros(num_pulses) 

print(input_data)
start_index = math.ceil(len(input_data)*0.5) #assumes a particular large amount of excess data
stop_index = math.ceil(len(input_data)*3/4)  #could be trimmed pre - running this program
for i in range (0, num_pulses):
	pulse_height = 0
	for j in range (start_index, stop_index): 
		if (input_data[j][i] > 0.002):
			if (input_data[j][i] > pulse_height):
				pulse_height = input_data[j][i]
	pulse_heights[i] = pulse_height

bin_size = 0.002 #2mV bin size
x_axis = np.zeros(400)
for i in range(1, len(x_axis)):
	x_axis[i] = x_axis[i-1] + bin_size

#export histogram
plt.hist(pulse_heights, bins = x_axis)
plt.title("Pulse Heights")
plt.xlabel("Voltage (V)")
plt.ylabel("Number of Pulses")
plt.savefig(r"C:\Users\sebas\OneDrive\Documents\Yang\PulseTestOutput2.png")
plt.show()
