import numpy as np
import matplotlib.pyplot as plt
import math
import scipy
from scipy.fftpack import rfft, irfft, fftfreq

def FFTandFilter(input_data, pulse_heights):						#runs the FFT filter and the generates a 
	height_index = 0												#pulse height array in pulse_heights
	pulse_index_start = 0											#histogram binning happens later
	pulse_time_start = input_data[0,0]
	print_flag = False
	filter_flag = True

	for i in range (len(input_data)):
		if (input_data[i][0] > pulse_time_start + 1E-3):			 #this means a new pulse
			if (filter_flag):
				current_pulse = input_data[pulse_index_start:(i-1),1]
				current_pulse_time = input_data[pulse_index_start:(i-1),0]
				#FFT Band Pass Filter
				f_spectrum = fftfreq(len(current_pulse), d = 0.02E-6) #just for plotting, is the freq range
				f_signal = rfft(current_pulse)						 #Fourier transform
				cut_f_signal = f_signal.copy()
				#cut_f_signal[(f_spectrum > 760849)] = 0			 #High Pass Filter
				#cut_f_signal[(f_spectrum < 33646)] = 0				 #Low Pass Filter
				cut_f_signal[(f_spectrum < 0)] = 0
				#cut_f_signal[(f_spectrum > 1000000)] = 0
				cut_signal = irfft(cut_f_signal) 					 #final signal
				if (print_flag):									 #Check the transform once
					plt.subplot(221)
					plt.plot(f_spectrum,f_signal)
					plt.xlim(-2E5,5E5)
					plt.subplot(222)
					plt.plot(f_spectrum,cut_f_signal)
					plt.xlim(-2E5,5E5)
					plt.subplot(223)
					plt.plot(current_pulse_time,current_pulse)
					plt.subplot(224)
					plt.plot(current_pulse_time,cut_signal)
					plt.show()
					print_flag = False
			else:
				cut_signal = input_data[pulse_index_start:(i-1),1]
		
			pulse_heights[height_index] = np.amax(cut_signal)
			pulse_time_start = input_data[i,0]
			height_index += 1
			pulse_index_start = i

input_1 = np.genfromtxt(r"C:\Users\sebas\OneDrive\Documents\Yang\cold_run_2.txt", delimiter = ",")
full_output_data = np.zeros(4000)
FFTandFilter(input_1, full_output_data[0:2000])
input_2 = np.genfromtxt(r"C:\Users\sebas\OneDrive\Documents\Yang\cold_run_1.txt", delimiter = ",")
FFTandFilter(input_2, full_output_data[2000:4000])

#export histogram
plt.hist(full_output_data, bins = 700)
plt.title("2-Run Cold Data, No Amp, FFT (>0)")
plt.xlabel("Voltage (V)")
#plt.xlim(0.01, 0.02)
plt.ylabel("Number of Pulses")
plt.savefig(r"C:\Users\sebas\OneDrive\Documents\Yang\ColdNoAmpEarly4000.png")
plt.show()
