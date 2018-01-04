from ROOT import gROOT, TCanvas, TH1F, TChain, TLegend
import os, sys

#c1 = TCanvas('c1','DCR90 Distribution',200,200)
#c1.Range(-0.01,0.01,0,1000)
#TH1F* dist = new TH1F("dist","DCR90 Distribution",100,-0.01,0.01)

TString runrange1,runrange2 # Used for each run in the first run range
int run1Start = 30059 # First run used in the run range
int run1End = 30077 # Last run used in the run range
int run2Start = 30328
int run2End = 30346
calibrationSkim1 = TChain("skimTree","skimTree")
calibrationSkim2 = TChain("skimTree","skimTree")

# Build the first run range's TChain
for i in range(run1Start, run1End+1):
        runrange1.Form("/global/project/projectdirs/majorana/data/mjd/surfmjd/analysis/skim/DS6cal/GAT-v01-06/skimDS6_run%d_small.root",i)
        calibrationSkim1.Add(runrange1)

# Build the second run range's TChain
for i in range(run2Start, run2End+1):
        runrange2.Form("/global/project/projectdirs/majorana/data/mjd/surfmjd/analysis/skim/DS6cal/GAT-v01-06/skimDS6_run%d_small.root",i)
        calibrationSkim2.Add(runrange2)

# Want to draw dcr90 / dcr99?
# calibrationSkim1.Draw("dcr90","trapENFCal < 2625 && trapENFCal > 2605 && channel == 1106" )

TString cutStr, drawStr;
# Or just draw dcr90 vs channel and get slices
drawStr.Form("dcr90:channel")

# MAKE SURE THIS HAS THE CORRECT CUTS
cutStr.Form("trapENFCal < 2635 && trapENFCal > 2605 && isGood && !wfDCBits && !muVeto && mH == 1")

# Draw everything for both run ranges
calibrationSkim1.Draw(drawStr, cutStr)
TH1F* range1 = gROOT->FindObject("htemp")
range1->SetAxisRange(-0.005,0.005,"Y")
# Should I set scale manually to be safe?
calibrationSkim2.Draw(drawStr, cutStr)
TH1F* range2 = gROOT->FindObject("htemp")
range2->SetAxisRange(-0.005,0.005,"Y")
# How do I save this? htemp?

# Do graphs with comparisons between run ranges? YES
TCanvas *c1 = new TCanvas("c1","c1",800,800)
range1->Draw();
range1->SetLineColor(kRed)
range2->Draw("same")
range2->SetLineColor(kBlue)
# Legend? Put info in here about which calibration runs were used
legend = new TLegend(0.7,0.7,0.9,0.9)
TString leg1,leg2
leg1.Form("Run Range %d - %d", run1Start, run1End)
leg2.Form("Run Range %d - %d", run2Start, run2End)
legend->AddEntry(range1, leg1, "l")
legend->AddEntry(range2, leg2, "l")

c1->Update()

# Save stuff here after looping?
TString fileName
fileName1.Form("/global/projecta/projectdirs/majorana/users/salvis/analysis/PZ_code/plots/DCRcomp.pdf")
fileName2.Form("/global/projecta/projectdirs/majorana/users/salvis/analysis/PZ_code/plots/DCRcomp.gif")
c1->SaveAs(fileName1)
c1->SaveAs(fileName2)
