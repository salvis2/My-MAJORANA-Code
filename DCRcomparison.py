# To run from the command line, type:
# python DCRcomparison.py [int1] [int2] [int3] [int4]
#
# To submit as a job to PDSF, copy /global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/runscripts/runComp.csh into your directory
# Then, type:
# echo [int1] [int2] [int3] [int4] | xargs sbatch runComp.csh
#
# Currently, the destination folder is hard-coded
#
# This script will take two run ranges as defined by [int1,int2] and [int3,int4]
# and generate TChains for each run range, then make a histogram of DCR90
# for each channel, then package all the graphs into 1 pdf file

from ROOT import TH1F, TH2F, TPad, TCanvas, TChain, TLegend, TLine, TAxis, TLatex, TPDF
from ROOT import gROOT, gPad
import os, sys
import pdb, argparse

# Add in an argument for the destination folder
# Parse arguments, 4 ints, as the closed boundaries of both run ranges
parser = argparse.ArgumentParser(description='This program takes two sets of runs and prints DCR distributions for each of them.', usage = '%(prog)s runRange1Start runRange1End runRange2Start runRange2End', epilog = 'Ex: python DCRcomparison.py 30059 30077 30328 30346')
parser.add_argument('boundaries', type = int, nargs = 4, help = 'These are the closed boundaries for both run sets')
args = parser.parse_args()

# Setup variables
firstruns = ""
secondruns = ""# Used for each run in the first run range
run1Start = args.boundaries[0] # First run used in the run range
run1End = args.boundaries[1] # Last run used in the run range
run2Start = args.boundaries[2]
run2End = args.boundaries[3]
calibrationSkim1 = TChain("skimTree","skimTree")
calibrationSkim2 = TChain("skimTree","skimTree")

# Build the first run range's TChain
for i in range(run1Start, run1End+1):
        firstruns = "/global/project/projectdirs/majorana/data/mjd/surfmjd/analysis/skim/DS6cal/GAT-v01-06/skimDS6_run%d_small.root" % i
        calibrationSkim1.Add(firstruns,0)

# Build the second run range's TChain
for i in range(run2Start, run2End+1):
        secondruns = "/global/project/projectdirs/majorana/data/mjd/surfmjd/analysis/skim/DS6cal/GAT-v01-06/skimDS6_run%d_small.root" % i
        calibrationSkim2.Add(secondruns,0)

# Want to draw dcr90 / dcr99?
# calibrationSkim1.Draw("dcr90","trapENFCal < 2625 && trapENFCal > 2605 && channel == 1106" )

#cutStr, drawStr = "","";
# Just draw dcr90 vs channel and get slices
#drawStr ="dcr90:channel>>range1"

# MAKE SURE THIS HAS THE CORRECT CUTS
cutStr = "trapENFCal < 2635 && trapENFCal > 2605 && isGood && !wfDCBits && !muVeto && mH == 1"

# DONT NEED ANYTHING IN HERE RIGHT NOW
# Draw everything for both run ranges
#c1 = TCanvas("c1","c1",800,800)

#pad1 = TPad('pad1', "first run range, low channels", 0.03,0.52,0.50,0.95)
#pad2 = TPad('pad2', "first run range, high channels", 0.51,0.52,0.98,0.95)
#pad3 = TPad('pad3', "second run range, low channels", 0.03,0.02,0.50,0.51)
#pad4 = TPad('pad4', "second run range, high channels",0.51,0.02,0.98,0.51)

#pad1.Draw()
#pad2.Draw()
#pad3.Draw()
#pad4.Draw()

# First run set, lower channels
#pad1.cd()
#range1 = TH2F("range1","First Run Set", 200, 550, 750, 1000,-0.005,0.005)
#cut1 = cutStr + " && channel < 800"
#calibrationSkim1.Draw(drawStr, cut1)
#range1.SetMarkerStyle(21)
#range1.Draw('COLZ')

# First run set, higher channels
#pad2.cd()
#drawStr = "dcr90:channel>>range2"
#range2 = TH2F("range2", "First Run Set",300, 1050, 1350, 1000, -0.005, 0.005)
#cut2 = cutStr + " && channel > 800"
#calibrationSkim1.Draw(drawStr, cut2)
#range2.SetMarkerStyle(21)
#range2.Draw('COLZ')

# Second run set, lower channels
#pad3.cd()
#drawStr = "dcr90:channel>>range3"
#range3 = TH2F("range3", "Second Run Set",200,550,750,1000,-0.005,0.005)
#cut3 = cutStr + "&& channel < 800"
#calibrationSkim2.Draw(drawStr,cut3)
#range3.SetMarkerStyle(21)
#range3.Draw('COLZ')

# Second run set, higher channels
#pad4.cd()
#drawStr = "dcr90:channel>>range4"
#range4 = TH2F("range4", "Second Run Set",300,1050,1350,1000,-0.005,0.005)
#cut4 = cutStr + " && channel > 800"
#calibrationSkim2.Draw(drawStr,cut4)
#range4.SetMarkerStyle(21)
#range4.Draw('COLZ')

# Do graphs with comparisons between run ranges? YES
# Legend? Put info in here about which calibration runs were used
#legend = TLegend(0.7,0.7,0.9,0.9)
#leg1,leg2 = "",""
#leg1 = "Run Range %d - %d" % (run1Start, run1End)
#leg2 = "Run Range %d - %d" % (run2Start, run2End)
#legend.AddEntry(range1, leg1, "l")
#legend.AddEntry(range2, leg2, "l")
#legend.Draw()
#c1.Update()

# Save files
#fileName1 = "/global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/plots/DCRcomp%d-%d_and_%d-%d.root" % (run1Start, run1End, run2Start, run2End)
#fileName2 = "/global/projecta/projectdirs/majorana/users/salvis/analysis/PZ_code/plots/DCRcomp%d-%d_and_%d-%d.gif" % (run1Start, run1End, run2Start, run2End)
#c1.SaveAs(fileName1)
#c1.SaveAs(fileName2)

# FOR LOOP
# Draw individual comparisons between the two run ranges for individual channels
# channel list from the built data in P3LTP
chanList = [680,681,678,679,674,675,672,673,632,633,630,631,626,627,690,691,692,693,648,649,640,641,642,643,664,665,662,663,660,661,658,659,616,617,610,611,608,609,584,585,600,601,598,599,592,593,696,697,624,625,628,629,688,689,694,695,614,615,1122,1123,1108,1109,1106,1107,1128,1129,1204,1205,1110,1111,1126,1127,1124,1125,1202,1203,1170,1171,1172,1173,1174,1175,1176,1177,1168,1169,1120,1121,1206,1207,1208,1209,1232,1233,1236,1237,1238,1239,1234,1235,1328,1329,1298,1299,1296,1297,1302,1303,1332,1333,1268,1269,1304,1305,1330,1331]
#chanList = [1204,1174,1173]
c2 = TCanvas('c2','c2',400,400)
# Can I just draw out here and then take slices in the loop?

for channel in chanList:
        # Check a single channel and draw overlapping DCR hists
        # Draw the first run set
        c2.Clear()
        histname1 = "hist1_chan%d" % channel
        histname2 = "hist2_chan%d" % channel

        # Can we make this faster?
        drawStr = "dcr90>>%s" % histname1
        cut1 = cutStr + " && channel == %d" % channel
        hist1 = TH1F(histname1, 'Channel %d DCR Comparison' % channel,1000, -0.001,0.001)
        calibrationSkim1.Draw(drawStr,cut1)
        hist1.SetLineColor(30)
        gPad.SetLogy()
        hist1.SetStats(False)
        xaxis1 = hist1.GetXaxis()
        # xaxis1.SetTitle("DCR90")
                # hist1.GetYaxis().SetTitle("Count")
        xaxis1.SetLabelSize(0.02)
        hist1.Draw()

        # Get the dcr90 value by integrating the hist
        minbin = xaxis1.FindBin(-0.001)
        maxbin = xaxis1.FindBin(0.001)
        zerobin = xaxis1.FindBin(0)
        goodintegral1 = hist1.Integral(minbin,zerobin)
        totalintegral1 = hist1.Integral(minbin,maxbin)
        # Don't divide by zero
        if (goodintegral1 != 0):
                dcr90_1 = goodintegral1/totalintegral1
        else:
                dcr90_1 = 0

        # Draw the second run set
        drawStr = "dcr90>>%s" % histname2
        hist2 = TH1F(histname2, 'Channel %d DCR Comparison' % channel, 1000,-0.001,0.001)
        calibrationSkim2.Draw(drawStr,cut1,"SAME")
        hist2.SetLineColor(45)
        gPad.SetLogy()
        hist2.SetStats(False)
        xaxis2 = hist2.GetXaxis()
        xaxis2.SetLabelSize(0.02)
        # xaxis2.SetTitle("DCR90")
        # hist2.GetYaxis().SetTitle("Count")
        hist2.Draw("SAME")

        # Get the second dcr90 value
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
        # Draw vertical line at dcr90 = 0 for reference
        c2.Update()
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
        c2.Update()
        fileName = "/global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/plots/DCRcompforRuns%d-%d_and_%d-%d.pdf" % (run1Start,run1End,run2Start,run2End)
        if(channel == chanList[0]):
                fileName += "("
        if(channel == chanList[len(chanList)-1]):
                fileName +=")"
        title = "Title: Channel %d" % channel
        c2.Print(fileName,title)

        # Save as individual files (not right now)
        #c2.Update()
        #fileName3 = "/global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/plots/DCRcompchannel%dforRuns%d-%d_and_%d-%d.pdf" % (channel, run1Start,run1End,run2Start,run2End)
        #c2.SaveAs(fileName3)
