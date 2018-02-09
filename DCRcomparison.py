# Module to take two run ranges and draw DCR histograms comparing the run ranges for each channel
# Will output a text file of the form 'eff_sheet_%d-%d.txt'
# These need to be concatenated before eff_chan_plotter.py is run
#
# To run from the command line, type:
# python DCRcomparison.py [int1] [int2] [int3] [int4] [destination folder]
#
# To submit as a job to PDSF, copy /global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/runscripts/runComp.csh into your directory
# Then, type:
# echo [int1] [int2] [int3] [int4] [dest_folder] | xargs sbatch runComp.csh
#
# Input the destination folder as an absolute path, ie:
# /global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/plots/
#
# This script will take two run ranges as defined by [int1,int2] and [int3,int4]
# and generate TChains for each run range, then make a histogram of DCR90
# for each channel, then package all the graphs into 1 pdf file

from ROOT import TH1F, TH2F, TPad, TCanvas, TChain, TLegend, TLine, TAxis, TLatex, TPDF, THStack
from ROOT import gROOT, gPad
import os, sys
import pdb, argparse

# Add in an argument for the destination folder
# Parse arguments, 4 ints, as the closed boundaries of both run ranges
#parser = argparse.ArgumentParser(description='This program takes two sets of runs and prints DCR distributions for each of them.', usage = '%(prog)s runRange1Start runRange1End runRange2Start runRange2End', epilog = 'Ex: python DCRcomparison.py 30059 30077 30328 30346')
#parser.add_argument('boundaries', type = int, nargs = 4, help = 'These are the closed boundaries for both run sets')
#parser.add_argument('dest_folder', help = 'This is where you want the files to end up')
#args = parser.parse_args()

def DCRComp(run1Start,run1End,run2Start,run2End,filePath):
# Setup variables

  firstruns = ""
  secondruns = ""# Used for each run in the first run range
  calibrationSkim1 = TChain("skimTree","skimTree")
  calibrationSkim2 = TChain("skimTree","skimTree")

  # Destination folder, trying to prevent a common formatting error
  if (filePath[-1] != '/'): filePath += '/'
  fileName = filePath + "DCRcompforRuns%d-%d_and_%d-%d.pdf" % (run1Start,run1End,run2Start,run2End)

  # Add functionality for multiple datasets?
  # NOTE: Be wary of comparing across multiple datasets. This hasn't been tested yet
# So far, only datasets 5 and 6 are known by the program (see below)
  skimPath1 = "/global/project/projectdirs/majorana/data/mjd/surfmjd/analysis/skim/"
  skimPath2 = "/global/project/projectdirs/majorana/data/mjd/surfmjd/analysis/skim/"

  runBoundariesDS5cM1 = [24305,24318,24539,24552,24761,24775,24971,24984,25248,25261,25479,25492]
  runBoundariesDS5cM2 = [23960,23970,24322,24332,24556,24567,24779,24789,24988,24998,25265,25275,25496,25506]

  # MAKE SURE THIS HAS THE CORRECT CUTS
  cuts = "trapENFCal < 2635 && trapENFCal > 2605 && isGood && !wfDCBits && !muVeto && mH == 1"
  # If there is only one module being calibrated in DS5
  cutStr5cM1 = " && C == 1"
  cutStr5cM2 = " && C == 2"

  if (run1Start <= 25507 and run1Start > 18712): # DS5c
    skimPath1 += "DS5ccal/GAT-v01-07-164-g8e0a877/skimDS5_"
    if (run1Start in runBoundariesDS5cM1): cuts += cutStr5cM1
    if (run1Start in runBoundariesDS5cM2): cuts += cutStr5cM2
    else: raise ValueError('First run boundary is not in either DS5c calibration range')

  if (run1Start > 25507): # DS6
    skimPath1 += "DS6cal/GAT-v01-06/skimDS6_"

  if (run2Start <= 25507 and run2Start > 18712): # DS5c
    skimPath2 += "DS5ccal/GAT-v01-07-164-g8e0a877/skimDS5_"
    if (run1Start in runBoundariesDS5cM1): cuts += cutStr5cM1
    if (run1Start in runBoundariesDS5cM2): cuts += cutStr5cM2
    else: raise ValueError('First run boundary is not in either DS5c calibration range')

  if (run2Start > 25507): # DS6
    skimPath2 += "DS6cal/GAT-v01-06/skimDS6_"

  cutStr = cuts
  # Build the first run range's TChain
  for i in range(run1Start, run1End+1):
        firstruns = skimPath1 + "run%d_small.root" % i
        calibrationSkim1.Add(firstruns,0)

  # Build the second run range's TChain
  for i in range(run2Start, run2End+1):
        secondruns = skimPath2 + "run%d_small.root" % i
        calibrationSkim2.Add(secondruns,0)

  # channel list from the built data in P3LTP
  # I don't need to use this now, but can check against it
  # IE check that every channel in this list has data
  # and that every channel with data is in this list
  chanList = [680,681,678,679,674,675,672,673,632,633,630,631,626,627,690,691,692,693,648,649,640,641,642,643,664,665,662,663,660,661,658,659,616,617,610,611,608,609,584,585,600,601,598,599,592,593,696,697,624,625,628,629,688,689,694,695,614,615,1122,1123,1108,1109,1106,1107,1128,1129,1204,1205,1110,1111,1126,1127,1124,1125,1202,1203,1170,1171,1172,1173,1174,1175,1176,1177,1168,1169,1120,1121,1206,1207,1208,1209,1232,1233,1236,1237,1238,1239,1234,1235,1328,1329,1298,1299,1296,1297,1302,1303,1332,1333,1268,1269,1304,1305,1330,1331]

  # Test case channel list
  #chanList = [1204,1174,1173]

  # Draw the whole dcr distribution vs channel
  # make sure there are enough bins that each channel is one bin
  c2 = TCanvas('c2','c2',400,400)
  drawStr = "dcr90:channel>>bighist1"
  bighist1 = TH2F("bighist1", "All Channels DCR Comparison",800,550,1350,1000,-0.001,0.001)
  calibrationSkim1.Draw(drawStr,cutStr,"COLZ")
  bighist1.SetLineColor(30)
  bighist1.SetStats(False)
  bighist1.GetXaxis().SetTitle("Channel")
  bighist1.GetYaxis().SetTitle("DCR99")
  bighist1.GetYaxis().SetTitleOffset(2.1)

  drawStr = "dcr90:channel>>bighist2"
  bighist2 = TH2F("bighist2", "All Channels DCR Comparison",800,550,1350,1000,-0.001,0.001)
  calibrationSkim2.Draw(drawStr,cutStr, "SAME COLZ")
  bighist2.SetLineColor(45)
  bighist2.SetStats(False)
  bighist2.GetXaxis().SetTitle("Channel")
  bighist2.GetYaxis().SetTitle("DCR99")
  bighist2.GetYaxis().SetTitleOffset(2.1)
  c2.SetLogz()
  gPad.SetLeftMargin(0.15)
  gPad.SetRightMargin(0.12)

  # Fix the different z scales
  maxz = max(bighist1.GetMaximum(),bighist2.GetMaximum())
  bighist1.GetZaxis().SetRangeUser(0,maxz)
  bighist2.GetZaxis().SetRangeUser(0,maxz)
  c2.Update()

  # Save the big TH2F as a root file
  rootfileName = filePath + "DCRcomp%d-%d_and_%d-%d.root" % (run1Start, run1End, run2Start, run2End)
  c2.SaveAs(rootfileName)

  # Start the big pdf
  c2.Print(fileName + "(","Title: All Channels")
  c2.Close()

  # TCanvas for the individual channels
  c3 = TCanvas('c3','c3', 400, 400)
  c3.cd()

  # Make txt file for chanList problems
  txtFileTitle = "channelProblemsforRuns%d-%d_and_%d-%d.txt" % (run1Start,run1End,run2Start,run2End)
  chanFile = open(txtFileTitle,"w+")

  # Want a hist of all DCR90 efficiencies for the run range
  # Only do this for the second run range (so I'm not doubling the plot)
  # Remove entries from this if they don't have any results
  active_channels = [680,681,678,679,674,675,672,673,632,633,630,631,626,627,690,691,692,693,648,649,640,641,642,643,664,665,662,663,660,661,658,659,616,617,610,611,608,609,584,585,600,601,598,599,592,593,696,697,624,625,628,629,688,689,694,695,614,615,1122,1123,1108,1109,1106,1107,1128,1129,1204,1205,1110,1111,1126,1127,1124,1125,1202,1203,1170,1171,1172,1173,1174,1175,1176,1177,1168,1169,1120,1121,1206,1207,1208,1209,1232,1233,1236,1237,1238,1239,1234,1235,1328,1329,1298,1299,1296,1297,1302,1303,1332,1333,1268,1269,1304,1305,1330,1331]
  active_channels = sorted(active_channels)
  active_chan_effs = []

  # Channel loop
  for channel in range(550,1351):
      # Conver channel to a bin number for slices
      bigX = bighist1.GetXaxis()
      currentbin = bigX.FindBin(channel)

      # Hack to get all the titles properly in the pdf
      canvastitle = "Channel %d" % channel
      bighist1.SetTitle(canvastitle)
      bighist2.SetTitle(canvastitle)

      # Get slices / bin content for each channel (the x axis of bighist)
      histname1 = "hist1_chan%d" % channel
      histname2 = "hist2_chan%d" % channel
      hist1 = bighist1.ProjectionY(histname1,currentbin,currentbin,"d")
      hist2 = bighist2.ProjectionY(histname2,currentbin,currentbin,"d")

      # Only proceed if the hists aren't empty
      if ((hist1.GetEntries() == 0 and hist2.GetEntries() == 0)):
      # Check that every empty channel isn't in chanList
        if (channel in chanList):
                chanFile.write("Channel %d has no output for runs %d - %d and %d - %d \n" % (channel, run1Start, run1End, run2Start, run2End))
                active_channels.remove(channel)

      else:
        # Make sure every channel with output is in chanList
        if (channel not in chanList):
                chanFile.write("Channel %d is not in chanList \n" % channel)

        c3.Clear()
        c3.SetTitle(canvastitle)
        hstack = THStack("hstack","")
        hstack.SetTitle(canvastitle)
        hist1.SetLineColor(40)
        gPad.SetLogy()
        hstack.Add(hist1)

        # Get the dcr99 value by integrating the hist
        xaxis1 = hist1.GetXaxis()
        minbin = xaxis1.FindBin(-0.001)
        maxbin = xaxis1.FindBin(0.001)
        zerobin = xaxis1.FindBin(0)
        goodintegral1 = hist1.Integral(minbin,zerobin)
        totalintegral1 = hist1.Integral(minbin,maxbin)
        # Don't divide by zero
        if (goodintegral1 != 0):
          dcr90_1 = goodintegral1/totalintegral1
        else :
          dcr90_1 = 0

        hist2.SetLineColor(30)
        hstack.Add(hist2)

        # Get the second dcr99 value
        xaxis2 = hist2.GetXaxis()
        minbin = xaxis2.FindBin(-0.001)
        maxbin = xaxis2.FindBin(0.001)
        zerobin = xaxis2.FindBin(0)
        goodintegral2 = hist2.Integral(minbin,zerobin)
        totalintegral2 = hist2.Integral(minbin,maxbin)
        # Don't divide by zero
        if (goodintegral2 != 0):
          dcr90_2 = goodintegral2/totalintegral2
        else:
          dcr90_2 = 0
        active_chan_effs.append(dcr90_2)

        # Formatting for the THStack
        hstack.Draw()
        xaxisStack = hstack.GetXaxis()
        xaxisStack.SetTitle("DCR99")
        hstack.GetYaxis().SetTitle("Count")
        xaxisStack.SetLabelSize(0.02)
        xaxisStack.SetTitleOffset(1.2)

        # Draw vertical line at dcr90 = 0 for reference
        c3.Update()
        ymax = max(hist1.GetMaximum(), hist2.GetMaximum())
        vert = TLine(0,0,0,ymax)
        vert.SetLineColor(2)
        vert.Draw()

        # Draw the legend
        chanlegend = TLegend(0.6,0.8,0.9,0.9)
        entry1 = chanlegend.AddEntry(hist1, "#splitline{Run Range %d - %d}{%f Efficiency}" % (run1Start, run1End, dcr90_1), "l")
        entry2 = chanlegend.AddEntry(hist2, "#splitline{Run Range %d - %d}{%f Efficiency}" % (run2Start, run2End, dcr90_2), "l")
        # If the Efficiencies differ by more than 1%, make their text red
        if (abs(dcr90_1 - dcr90_2) > 0.01):
          entry1.SetTextColor(2)
          entry2.SetTextColor(2)
        entry1.SetTextSize(0.02)
        entry2.SetTextSize(0.02)
        chanlegend.Draw()

        # Save as one big pdf file
        pagetitle = "Title: " + canvastitle
        c3.Update()
        c3.Print(fileName,pagetitle)

  # Close the pdf with a blank page
  c3.Clear()
  c3.Print(fileName + ")","I need to close the document somehow")
  c3.Close()

  # I want a spreadsheet of all the DCR90 efficiencies
  # Will make a file for each calibration run set, and then concatenate them later
  spreadsheetfilename = filePath + "eff_sheet_%d-%d.txt" % (run2Start,run2End)
  spreadsheet = open(spreadsheetfilename,"w+")

  # Make the dcr90 efficiency plot for the second run set only
  c_eff = TCanvas('c_eff','c_eff',800,400)
  c_eff.cd()

  # active_channels should be the x-axis labels
  # active_chan_effs should be the y-values
  num_chan = len(active_channels)
  eff_hist = TH1F('eff_hist',"DCR99 Efficiencies for Calibration Runs %d-%d" % (run2Start, run2End),num_chan,0,num_chan)
  eff_xaxis = eff_hist.GetXaxis()

  # Input data and write to the spreadsheet
  for i in range(0,num_chan):
    eff_xaxis.SetBinLabel(i+1, str(active_channels[i]))
    eff_hist.SetBinContent(i+1,active_chan_effs[i])
    spreadsheet.write("%d  %d  %d  %f  \n" % (run2Start,run2End,active_channels[i],active_chan_effs[i]))

  c_eff.SetGridx()
  eff_hist.SetStats(False)
  eff_xaxis.SetLabelSize(0.03)
  eff_xaxis.SetTitle("Channel")
  eff_xaxis.SetTitleOffset(1.4)
  eff_hist.GetYaxis().SetTitle("DCR99 Efficiency")
  eff_hist.Draw()
  c_eff.Update()

  # Save
  eff_fileName = filePath + "DCR99_Efficiencies_Runs_%d-%d.pdf" % (run2Start,run2End)
  eff_title = "DCR99 Efficiencies for Calibration Runs %d-%d" % (run2Start, run2End)
  c_eff.SaveAs(eff_fileName,eff_title)
  c_eff.Close()
  spreadsheet.close()

if __name__ == "__main__":
  DCRComp(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),str(sys.argv[5]))
