# My-MAJORANA-Code
Code that primarily I have developed for the MAJORANA Collaboration. 

full_eff_plotter.py is the capstone script, running DCRcomparison.py and eff_chan_plotter.py. 
It is submitted to a supercomputer via runFullComp.csh and submitFullCompJob.csh.
The script will generate plots comparing the DCR parameter between two adjacent calibration run ranges for each individual detector, then generate a set of plots showing the efficiency of the DCR cut over all calibration run ranges for each individual detector.

angery.py and specificEffplots.py are scripts that were run once to achieve a set of job submission commands and to get specific graphs in a smaller file.

DCRplotter.cc is a very similar program to full_eff_plotter.py, except that it is written in C++ and packages graphs for each detector, instead of each calibration run.

DCR2dplotter.cc is a script that visualizes a lot of data for 5 problem detectors that I have worked with.

All of the .csh scripts are for submitting jobs to the supercomputer PDSF. Some of them reference programs that I did not make, and thus aren't shown here.
