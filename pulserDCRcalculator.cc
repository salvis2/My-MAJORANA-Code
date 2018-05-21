#include <iostream>
#include <stdlib.h>
#include <string>
#include <complex>
#include <vector>
#include <TH1.h>
#include "TH2D.h"
#include <TFile.h>
#include <TStyle.h>
#include <TString.h>
#include <TTree.h>
#include <TLegend.h>
#include <TCanvas.h>
#include <TLine.h>
#include <TPad.h>
#include <TChain.h>
#include <TGraph.h>
#include <TLegendEntry.h>
#include <TProfile.h>
#include <TF1.h>
#include <TLatex.h>
#include <TFitResultPtr.h>
#include "GATDataSet.hh"
//#include <DataSetInfo.hh>
#include "DataSetInfo.hh"
#include <THStack.h>

using namespace std;

int main(int argc, char* argv[]){

  if (argc < 4){
    cout << "Usage: " << argv[0] << " 'chan' 'runStart' 'runEnd'" << endl;
    return 1;
  }

  double chan = stod(argv[1]);
  int runStart = atoi(argv[2]);
  int runEnd = atoi(argv[3]);

  // Find gatified data for the run range
  // Don't overlap datasets, so go off of runStart
  TString pulserFolder,customFolder,inputFolder,gatFolder,pulserFile,pulserFile2,calFile,fileName,cuts,fineCuts,calCuts;

  vector< vector<unsigned int> > runBoundaries1(56, vector<unsigned int>(2));
  runBoundaries1 = {{9452,9468},{9495,9516},{9519,9534},{9683,9706},{9732,9757},{9788,9810},{9938,9949},{9968,9994},{9999,10013},{10040,10059},{10359,10373},{10403,10420},{10485,10495},{10498,10504},{10529,10547},{10721,10735},{10767,10785},{10801,10825},{10943,10957},{10983,10997},{11029,11042},{11068,11081},{11215,11226},{11307,11337},{11339,11348},{11506,11632},{11672,11683},{11799,11813},{11967,12009},{12470,12473},{12502,12510},{12627,12634},{12656,12662},{12726,12733},{12800,12809},{12863,12873},{12886,12998},{13058,13064},{13139,13146},{13287,13301},{13353,13360},{13385,13393},{13420,13428},{13551,13557},{13706,13713},{13690,13697},{13740,13747},{13773,13780},{13905,13912},{13954,13961},{13987,13994},{14093,14100},{14149,14154},{14180,14188},{14274,14282},{14374,14384}};

  vector< vector<unsigned int> > runBoundaries2(13, vector<unsigned int>(2));
  runBoundaries2 = {{14568,14575},{14699,14707},{14855,14861},{14927,14934},{15054,14060},{15119,15125},{15248,15254},{15330,15336},{15490,15506},{15627,15633},{15707,15714},{15789,15795},{15845,15858}};

  vector< vector<unsigned int> > runBoundaries5cm1(6, vector<unsigned int>(2));
  runBoundaries5cm1 =  {{24305,24318},{24539,24552},{24761,24775},{24971,24984},{25248,25261},{25479,25492}};

  vector< vector<unsigned int> > runBoundaries5cm2(7, vector<unsigned int>(2));
  runBoundaries5cm2 = {{23960,23970},{24322,24332},{24556,24567},{24779,24789},{24988,24998},{25265,25275},{25496,25506}};

  vector< vector<unsigned int> > runBoundaries6m1(52, vector<unsigned int>(52));
  runBoundaries6m1 = {{25690,25702},{25834,25935},{26042,26049},{26215,26236},{26381,26404},{26623,26646},{26750,26771},{26946,26967},{27180,27194},{27938,27951},{27975,27988},{28113,28133},{28322,28343},{28468,28608},{28970,28990},{29356,29376},{29525,29545},{29698,29718},{29915,29934},{30059,30077},{30328,30346},{31325,31343},{31685,31701},{31780,31791},{31919,31939},{32008,32015},{32024,32041},{32161,32178},{32416,32451},{32855,32884},{33060,33230},{33510,33526},{33654,33671},{33693,33710},{33910,33926},{34075,34091},{34271,34287},{34457,34471},{34501,34688},{34819,34835},{35031,35047},{35197,35215},{35366,35382},{35556,35739},{35913,35930},{35938,35945},{36108,36114},{36320,36329},{36539,36546},{36710,36719},{36888,36992},{37238,37246}};

  vector< vector<unsigned int> > runBoundaries6m2(52, vector<unsigned int>(52));
  runBoundaries6m2 = {{25676,25686},{25939,26020},{26042,26049},{26215,26236},{26381,26404},{26623,26646},{26750,26771},{26946,26967},{27180,27194},{27938,27951},{27975,27988},{28113,28133},{28322,28343},{28468,28608},{28970,28990},{29356,29376},{29525,29545},{29698,29718},{29915,29934},{30059,30077},{30328,30346},{31325,31343},{31685,31701},{31780,31791},{31919,31939},{32008,32015},{32024,32041},{32161,32178},{32416,32451},{32855,32884},{33060,33230},{33510,33526},{33654,33671},{33693,33710},{33910,33926},{34075,34091},{34271,34287},{34457,34471},{34501,34688},{34819,34835},{35031,35047},{35197,35215},{35366,35382},{35556,35739},{35913,35930},{35948,35953},{36117,36122},{36333,36340},{36551,36558},{36723,36731},{37004,37086},{37250,37257}};

  vector< vector<unsigned int> > runBoundaries;

  // Set Up Strings
  pulserFolder.Form("/global/project/projectdirs/majorana/data/mjd/surfmjd/analysis/pulser");
  fileName.Form("/global/projecta/projectdirs/majorana/users/salvis/analysis/PZ_code/plots/pulserShift_ch%d_run_%d-%d_fine.root",int(chan),runStart,runEnd);
  cuts.Form("Pulser != 0 && channel == %E",chan);
  calCuts.Form("EventDC1Bits != 0 && channel == %E",chan);
  fineCuts.Form(" && nlcblrwfSlope < -0.014 && trapENF < 1650 && trapENF > 100");
  customFolder.Form("/global/projecta/projectdirs/majorana/users/salvis/analysis/PZ_code/pulser_files_DS1");

  // Find the right detector string
  // Find the correct set of calibration runs to plot
  if (runStart >= 9422 && runStart <= 14502){
    inputFolder.Form("%s/P3KJR",pulserFolder.Data());
    gatFolder.Form("/global/project/projectdirs/majorana/data/mjd/surfmjd/data/gatified/P3KJR");
    runBoundaries = runBoundaries1;
    cout << "DataSet 1, Channel " << int(chan) << endl;
    }
  else if (runStart >= 14503 && runStart <= 15892){ // Don't actually need DS2
    inputFolder.Form("%s/P3KJR",pulserFolder.Data());
    gatFolder.Form("/global/project/projectdirs/majorana/data/mjd/surfmjd/data/gatified/P3KJR");
    runBoundaries = runBoundaries2;
    cout << "DataSet 2, Channel " << int(chan) << endl;
  }
  else if (runStart >= 20000 && runStart <= 25671){
    inputFolder.Form("%s/P3LQK",pulserFolder.Data());
    gatFolder.Form("/global/project/projectdirs/majorana/data/mjd/surfmjd/data/gatified/P3LQK");
    if (chan > 1000){ runBoundaries = runBoundaries5cm2; }
    else { runBoundaries = runBoundaries5cm1; }
    cout << "DataSet 5, Channel " << int(chan) << endl;
  }
  else if (runStart >= 25672 && runStart <= 37200){
    inputFolder.Form("%s/P3LTP",pulserFolder.Data());
    gatFolder.Form("/global/project/projectdirs/majorana/data/mjd/surfmjd/data/gatified/P3LTP");
    if (chan > 1000){ runBoundaries = runBoundaries6m2; }
    else { runBoundaries = runBoundaries6m1;}
    cout << "DataSet 6, Channel " << int(chan) << endl;
  }
  else {
    cout << "Invalid Run Start" << endl;
    return 0;
  }

  // pulserChain is for open/blind background events, and pulls from pulser data
  // calChain is for calibration events, and pulls from gatified data
  TChain* pulserChain = new TChain("pulsertree");

  for (int i = runStart; i < runEnd+1; i++){
    pulserFile.Form("%s/pulser_%d.root",inputFolder.Data(),i);
    TFile f(pulserFile);

    // Valid File
    if(!f.IsZombie()){
      TTree* pulsertree = (TTree*)f.Get("pulsertree");

      // Proper Size
      if (pulsertree->GetListOfBranches()->GetEntries() == 5){
	pulserChain->Add(pulserFile);
        cout << "n ";
      }
    }
  }

  if (runStart >= 9422 && runStart <= 14502){ // Only for DS1
    for (int i = runStart; i < runEnd+1; i++){
      pulserFile2.Form("%s/pulser_%d.root",customFolder.Data(),i);
      TFile f2(pulserFile2);

      if (!f2.IsZombie()){
        TTree* pulsertree = (TTree*)f2.Get("pulsertree");

        if (pulsertree->GetListOfBranches()->GetEntries() == 5){
          pulserChain->Add(pulserFile2);
          cout <<"c ";
        }
      }
    }
  }
  cout << endl;

  // First, find the cal run that starts just before the runStart var
  // and the cal run that ends right after the runEnd var
  // Hold the index of the first cal before the input var and the first cal after the 2nd input var
  int calStart=0, calEnd=0;
  for (int i = 0; i < runBoundaries.size(); i++){
    if (runBoundaries[i][0] > runStart && calStart == 0){calStart = i-1;}
    if (runBoundaries[i][1] > runEnd && calEnd == 0){calEnd = i;}
  }
  if (calStart < 0){calStart = 0;}
  if (calEnd == 0){calEnd = runBoundaries.size()-1;}

  int calRunStart = runBoundaries[calStart][0];
  if (calRunStart > runStart) {calRunStart = runStart;}

  int calRunEnd = runBoundaries[calEnd][1];
  if (calRunEnd < runEnd) {calRunEnd = runEnd;}

  cout << "Checking from index " << calStart << " to " << calEnd << endl;
  cout << "Checking from run " << calRunStart << " to " << calRunEnd << endl;

  // Loop over pulserChain, calling GetEntries(cuts+fineCuts+movingCut):
  // movingCut is something you increment until you only have 95% of the data left.

  int nEntries = pulserChain->GetEntries(cuts+fineCuts);
  TString movingCut;
  
  double hiSlope = pulserChain->GetMaximum("nlcblrwfSlope"), slopeChange = 0.0001;
  int cutEntries = nEntries;
  double fracRemain = 1.0*cutEntries/nEntries;
  double oldFracRemain = fracRemain;
  double frac99 = 0, frac96 = 0;
  double cut96slope=0.0, cut99slope=0.0;

  cout << "Beginning huge-ass while loop with a nlcblrwfSlope of " << hiSlope << endl;

  while (fracRemain > 0.96){
    oldFracRemain = fracRemain;
    hiSlope -= slopeChange;
    movingCut.Form(" && nlcblrwfSlope < %E",hiSlope);
    cutEntries = pulserChain->GetEntries(cuts+fineCuts+movingCut);
    fracRemain = 1.0*cutEntries/nEntries;

    if (slopeChange == 0.0001 && fracRemain <= 0.99){
      cout << "Reached nlcblrwfSlope of " << hiSlope << " cutting " << fracRemain << " of all events" << endl;
      cout << "Decreasing step size" << endl;
      hiSlope += slopeChange;
      slopeChange = 0.00001;
      fracRemain = oldFracRemain;
      continue;
    }

    else if (slopeChange == 0.00001 && cut99slope == 0 && fracRemain <= 0.99){
      cut99slope = hiSlope;
      frac99 = fracRemain;
      cout << "Remaining " << cutEntries <<" out of " << nEntries << " total, or "<< fracRemain <<", at nlcblrwfSlope max of " <<cut99slope<< " for the 0.99 cutoff"<<endl;
    }
  }
  cut96slope = hiSlope;
  frac96 = fracRemain;
  cout << "Remaining " << cutEntries <<" out of " << nEntries << " total, or "<< fracRemain <<", at nlcblrwfSlope max of " <<cut96slope<< " for the 0.96 cutoff" << endl;

  // GATDataSet for the detector string
  GATDataSet firstrun(35940);
  TString detPos, fracTitle, ampTitle;

  detPos = firstrun.GetChannelMap()->GetDetectorPos(chan);
  fracTitle.Form("Pulser Fractional Height for Ch %d, %s",int(chan),detPos.Data());

  // Set up canvas and pads
  TCanvas* pulserCanvas = new TCanvas("pulserCanvas","pulserCanvas",1200,600);
  pulserCanvas->Divide(2,1);
  pulserCanvas->cd(1);
  
  // Plot nlcblrwfSlope/trapENF vs run for the channel
  TH2D* rawPulserHist = new TH2D("rawPulserHist",fracTitle,calRunEnd-calRunStart+20,calRunStart-10,calRunEnd+10,3000,-0.000016,-0.00001);
  
  // Set up the hist for calChain
  // Draw all cal runs from the first index to the second index

  // Draw all the data
  pulserChain->Draw("nlcblrwfSlope/trapENF:run>>rawPulserHist",cuts+fineCuts);
  //calChain->Draw("nlcblrwfSlope:trapENF>>pulserEHist",calCuts);

  rawPulserHist->GetXaxis()->SetTitle("run");
  rawPulserHist->GetXaxis()->SetLabelSize(0.015);
  rawPulserHist->GetYaxis()->SetTitle("nlcblrwfSlope/trapENF, ~1/tao");
  rawPulserHist->GetYaxis()->SetLabelSize(0.015);

  // Draw the raw nlcblrwfSlope dist for a run early and a run in the shift, then draw a line at the 90% and the 95%
  // How do I convert that to fractional slope? How should I access the trapENF?
  // Early run: 26500 with trapENF of 1588, shift run: 28900 with trapENF of 1588
  TH1D* earlyHist = rawPulserHist->ProjectionY("",rawPulserHist->GetXaxis()->FindBin(runStart),rawPulserHist->GetXaxis()->FindBin(runEnd),"");
  //TH1D* shiftHist = rawPulserHist->ProjectionY("",rawPulserHist->GetXaxis()->FindBin(29120),rawPulserHist->GetXaxis()->FindBin(29220),"");
 
  double energy = 1550;

  if (chan == 1120){energy =1556.0;}
  else if (chan == 1232){energy = 1588.0;}
  else if (chan == 1330){energy = 1561.0;}
 
  double cut96frac = cut96slope/energy;
  double cut99frac = cut99slope/energy;  

  earlyHist->SetMarkerColor(4);
  //shiftHist->SetMarkerColor(2);

  THStack* pulserShift = new THStack("pulserShift","Pulser Acceptance Rates");
  pulserShift->Add(earlyHist);
  //pulserShift->Add(shiftHist);

  pulserCanvas->cd(2);
  pulserShift->Draw();

  pulserShift->GetXaxis()->SetTitle("nlcblrwfSlope/trapENF");
  pulserShift->GetYaxis()->SetTitle("Count");

  double min = pulserShift->GetMinimum();
  double max = pulserShift->GetMaximum();

  TLine* line96 = new TLine(cut96frac,min,cut96frac,max);
  TLine* line99 = new TLine(cut99frac,min,cut99frac,max);

  line96->SetLineColor(6);
  line99->SetLineColor(9);

  line96->Draw("SAME");
  line99->Draw("SAME");

  TString title96, title99, sepText;
  title96.Form("#splitline{%E Acceptance at}{nlcblrwfSlope of %E}",frac96,cut96slope);
  title99.Form("#splitline{%E Acceptance at}{nlcblrwfSlope of %E}",frac99,cut99slope);
  sepText.Form("#splitline{Difference of %E on the x-axis}{corresponds to a %E efficiency shift}",cut99frac-cut96frac,frac99-frac96);

  TLegend* leg = new TLegend(0.7,0.7,0.95,0.95);
  leg->AddEntry(earlyHist,sepText,"p");
  //leg->AddEntry(shiftHist,"Shift in Pulser Slope","p");
  leg->AddEntry(line96,title96,"l");
  leg->AddEntry(line99,title99,"l");
  leg->Draw("SAME");

  pulserCanvas->Update();
  //avgPulserHist->Draw();
  // rawPulserHist->Draw();
  // pulserEHist->Draw();
  pulserCanvas->SaveAs(fileName);
  delete pulserCanvas; 
  delete rawPulserHist;
  //delete pulserEHist;
  delete earlyHist;
  //delete shiftHist;
  delete line99;
  delete line96;
  delete pulserShift;
  delete leg;
 
  cout << "Exiting Pulser Calculator" << endl;

  return 1;
}
