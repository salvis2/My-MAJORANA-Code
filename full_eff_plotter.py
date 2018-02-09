# script that runs the DCR plotter and efficiency plotter one after the other for an entire dataset
#
# use from the command line as:
# python full_eff_plotter.py 'ds' 'dest_folder'
# ex. python full_eff_plotter.py DS6 /global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/plots/
#
# submit to PDSF as:
# I need to build a csh file for this

from ROOT import TH1F, TH2F, TPad, TCanvas, TChain, TLegend, TLine, TAxis, TLatex, TPDF, THStack
from ROOT import gROOT, gPad
import os, sys
import pdb, argparse
import DCRcomparison, eff_chan_plotter

# command line argument for which dataset to run?
parser = argparse.ArgumentParser(description = 'This program will plot DCR99 for each calibration run set against the previous calibration run set for all calibration run sets. The first calibration run set will be plotted against its first run.')
parser.add_argument('ds', help = 'Pick DS6, DS5cM1, or DS5cM2')
parser.add_argument('dest_folder', help = 'This is where you want the files to end up')
args = parser.parse_args()

runBoundariesDS6 = [[30059,30077],[30328,30346],[31325,31343],[31685,31701],[31780,31791],[31919,31939],[32008,32015],[32024,32041],[32161,32178],[32416,32451],[32855,32884],[33060,33230],[33510,33526],[33654,33671],[33693,33710]]

runBoundariesDS5cM1 = [[24305,24318],[24539,24552],[24761,24775],[24971,24984],[25248,25261],[25479,25492]]
runBoundariesDS5cM2 = [[23960,23970],[24322,24332],[24556,24567],[24779,24789],[24988,24998],[25265,25275],[25496,25506]]

# Select DataSet
runs = [[]]
ds6, ds5cm1, ds5cm2 = False, False, False
if (args.ds == 'DS6'):
  runs = runBoundariesDS6
  ds6 = True
elif (args.ds == 'DS5cM1'):
  runs = runBoundariesDS5cM1
  ds5cm1 = True
elif (args.ds == 'DS5cM2'):
  runs = runBoundariesDS5cM2
  ds5cm2 = True
else: raise ValueError('Invalid DataSet entry')

# for txt file output names
txtfileoutputs = []
# run DCRcomparison.py for the entire run range set of the desired DataSet
for i in range(len(runs)-1):
  if (i == 0):
    DCRcomparison.DCRComp(runs[i][0],runs[i][0],runs[i][0],runs[i][1],args.dest_folder)
    txtfileoutputs.append(args.dest_folder + "eff_sheet_%d-%d.txt" % (runs[i][0],runs[i][1]))
  DCRcomparison.DCRComp(runs[i][0],runs[i][1],runs[i+1][0],runs[i+1][1],args.dest_folder)
  txtfileoutputs.append(args.dest_folder + "eff_sheet_%d-%d.txt" % (runs[i+1][0],runs[i+1][1]))

# concatenate text file outputs from above
with open(args.dest_folder + 'eff_sheet.txt', 'w') as effsheet:
  for fname in txtfileoutputs:
    with open(fname) as infile:
      for line in infile:
        effsheet.write(line)

# run eff_chan_plotter.py
if (ds6): eff_chan_plotter.eff_plot(args.dest_folder, 'DS6')
elif (ds5cm1): eff_chan_plotter.eff_plot(args.dest_folder, 'DS5cM1')
elif (ds5cm2): eff_chan_plotter.eff_plot(args.dest_folder, 'DS5cM2')
else: raise ValueError('No dataset selected correctly u dinghus')
