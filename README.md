# My-MAJORANA-Code
Code that primarily I have developed for the MAJORANA Collaboration at the University of Washington.

## Python Programs

full_eff_plotter.py is the capstone Python script, running DCRcomparison.py and eff_chan_plotter.py. 
It is submitted to a supercomputer via CShell scripts.

The Python script will generate plots comparing the DCR parameter between two adjacent calibration run ranges for each individual detector, then generate a set of plots showing the efficiency of the DCR cut over all calibration run ranges for each individual detector.

## C++ Programs

DCRplotter.cc is a very similar program to full_eff_plotter.py, except that it is written in C++ and packages graphs for each detector, instead of each calibration run. It is significantly faster, and with some CShell scripts, can run a supercomputer-submitted job for each of ~40 detectors in parallel, which massively reduces runtime for large datasets.

pulserDCRcalculator.cc is a script that takes in a range of pulser data, then iterates until it can find what values of the axis correspond to 99% and 96% of the data. It is used to set a detector-specific level of acceptable instabilities in pulser data.

## Programs made at UIUC

The files PulseHeightFiltering.py and PulseFilteringLongWord.py were created while I was an undergraduate student. They took an output txt file from a oscilloscope and generated plots describing the distribution of pulse heights.
