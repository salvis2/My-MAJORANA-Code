import os, sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Read in the efficiency txt file
efficiencies = [[],[],[],[]]
with open("eff_sheet.txt") as efficiency_file:
    for line in efficiency_file:
        data = line.split()
        efficiencies[0].append(int(data[0]))
        efficiencies[1].append(int(data[1]))
        efficiencies[2].append(int(data[2]))
        efficiencies[3].append(float(data[3]))

with PdfPages('/global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/plots/spec4.pdf') as pdf:

    channels = [592,593]
    for chan in channels:
        # Find the range in array that corresponds to this channel
        chan_effs = [[],[],[],[]]
        for i in range(0,len(efficiencies[0])):
            if (efficiencies[2][i] == chan):
                for j in range (0,4):
                    chan_effs[j].append(efficiencies[j][i])

        if (chan == channels[0]): plt.plot(chan_effs[0],chan_effs[3],'ro', label = 'Chan %d' % chan)
        if (chan == channels[1]): plt.plot(chan_effs[0],chan_effs[3],'bs', label = 'Chan %d' % chan)

    plt.xlabel('Starting Run')
    plt.ylabel('DCR 90 Efficiency')
    plt.title('Channel %d/%d DCR 90 Efficiency' % (channels[0],channels[1]))
    plt.ylim(0,1)
    plt.legend()
    pdf.savefig()
    plt.close()
