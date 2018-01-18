import os, sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

# Read in the efficiency txt file
efficiencies = [[],[],[],[]]
with open("eff_sheet.txt") as efficiency_file:
    for line in efficiency_file:
        data = line.split()
        efficiencies[0].append(int(data[0]))
        efficiencies[1].append(int(data[1]))
        efficiencies[2].append(int(data[2]))
        efficiencies[3].append(float(data[3]))

# print(len(efficiencies)) # Gives 4
# print(len(efficiencies[0])) # Gives 1008

# efficiencies[0] = start runs
# efficiencies[1] = end runs
# efficiencies[2] = channels
# efficiencies[3] = dcr90 efficiencies

# Save to big pdf
with PdfPages('/global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/plots/Efficiencies_Over_Time.pdf') as pdf:
    # Want to plot each channel's efficiencies as a function of run
    # Sort the array by channel
    #indices = range(len(efficiencies[0]))
    #indices.sort(key = efficiencies[2].__getitem__)
    #for i, sublist in enumerate(efficiencies):
        #efficiencies[i] = [sublist[j] for j in indices]

    # Get something I can actually iterate over usefully
    channels = set(efficiencies[2])
    print(channels)
    channels = sorted(channels)
    print(channels)
    for chan in channels:
        # Find the range in array that corresponds to this channel
        chan_effs = [[],[],[],[]]
        for i in range(0,len(efficiencies[0])):
            if (efficiencies[2][i] == chan):
                for j in range (0,4):
                    chan_effs[j].append(efficiencies[j][i])

        plt.plot(chan_effs[0],chan_effs[3],'ro')
        plt.ylim(0,1)
        plt.title('Channel %d DCR 90 Efficiency Over Time' % chan)
        plt.xlabel('Starting Run')
        plt.ylabel('DCR 90 Efficiency')
        #plt.show()
        pdf.savefig()
        plt.close()
