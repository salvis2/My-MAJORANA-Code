# Module to take the concatenated outputs of DCRcomparison.DCRComp
# and plot efficiencies for each channel over all the calibration run ranges
# requires the existence of eff_sheet.txt

import os, sys, argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def eff_plot(dest_folder,ds):

  # Read in the efficiency txt file
  efficiencies = [[],[],[],[]]
  # ideally, dest_folder is /global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/plots/
  txtfile = dest_folder + "eff_sheet.txt"
  with open(txtfile) as efficiency_file:
      for line in efficiency_file:
        data = line.split()
        efficiencies[0].append(int(data[0]))
        efficiencies[1].append(int(data[1]))
        efficiencies[2].append(int(data[2]))
        efficiencies[3].append(float(data[3]))

  # efficiencies[0] = start runs
  # efficiencies[1] = end runs
  # efficiencies[2] = channels
  # efficiencies[3] = dcr90 efficiencies

  # Pdf name check
  pdf_name = dest_folder + 'Efficiencies_Over_Time_'
  if (ds == 'DS6'): pdf_name += 'DS6.pdf'
  elif (ds == 'DS5cM1'): pdf_name += 'DS5cM1.pdf'
  elif (ds == 'DS5cM2'): pdf_name += 'DS5cM2.pdf'
  else: raise ValueError('Incorrect DataSet')

  # Save to big pdf
  with PdfPages(pdf_name) as pdf:
      # Sort the array by channel
      channels = set(efficiencies[2])
      channels = sorted(channels)
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
        pdf.savefig()
        plt.close()

if __name__ == "__main__":
  eff_plot(str(sys.argv[1]),int(sys.argv[2]))
