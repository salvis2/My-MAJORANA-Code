/* DCRplotter.cc 
 * Updated DCRcomparison.py to C++
 * Takes in DataSet 5 or 6, a channel, and a GAT tag
 * Use as ./DCRplotter 'dataset' 'channel' 'GAT-v01-07-xxx-xxxxxxxx'
 * Ex. ./DCRplotter 5 584 GAT-v01-07-259-gffcbb0b
 *
 */

#include <iostream>
#include <stdlib.h>
#include <string>
#include <complex>
#include <vector>
#include "TH1.h"
#include <TF1.h>
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
#include "MJTChannelSettings.hh"
#include "GATDataSet.hh"
#include "MJTChannelMap.hh"
#include "TTree.h"
#include <TGraph.h>
#include "TGraph.h"
#include "TString.h"

using namespace std;

// Function to plot DCR distributions for a single channel over all calibration runs in the Dataset
int PlotDCR(int chan, int ds, TString gat_tag, vector< vector<unsigned int> > runranges){
  
  // Set up destination and input folders
  TString dest_folder, skim_folder, packet_title, skim_folder_check;
  if (ds == 5) {
    dest_folder.Form("/global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/plots/DS5c/dcr99");
    skim_folder.Form("/global/project/projectdirs/majorana/data/mjd/surfmjd/analysis/skim/DS5ccal/%s", gat_tag.Data());
  }
  else {
    dest_folder.Form("/global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/plots/DS%d/dcr99", ds);
    skim_folder.Form("/global/project/projectdirs/majorana/data/mjd/surfmjd/analysis/skim/DS%dcal/%s", ds, gat_tag.Data());
  }

  skim_folder_check.Form("%s",skim_folder.Data());
  if (skim_folder_check.Last('/') != skim_folder_check.Length()) {skim_folder.Form("%s/",skim_folder_check.Data());}
  packet_title.Form("%s/DS%d_dcrPacket_chan%d.pdf",dest_folder.Data(),ds,chan);

  // Get the number of rows in the runranges array
  int num_rows = runranges.size();

  // Add in array for efficiencies
  double efficiencies[num_rows];
  for(int i = 0; i<num_rows;i++){
    efficiencies[i] = 0;
  }
  // Cuts, more relevant if I need to plan to plot the compton region or other peaks
  TString cuts, skimfile; //, peakcuts;
  cuts.Form("isGood && trapENFCal > 2605 && trapENFCal < 2635 && !wfDCBits && !muVeto && mH == 1  && avse > -1 && !isLNFill1 && !isLNFill2 && channel == %d", chan);
  
  // Make TCanvas for skimHists
  TCanvas * c1 = new TCanvas("c1","c1",400,400);
  c1->cd();

  // Change the loop to plot a TH2D of dcr99 v run, then grab slices for the run ranges to make individual cal plots
  TChain* skimCalib = new TChain("skimTree");
  // Loop over each entry pair in runranges[][2]
  for (int i = 0; i < num_rows; i++){
    // Track min and max of each skimHist? Can I change that afterwards? Or do I just guess?
    // Currently guessing, -0.003 to 0.001
    //TChain* skimCalib = new TChain("skimTree");
    //TH1D* skimHist = new TH1D("skimHist",skimHistTitle,200,-0.003,0.001);

    // Run range is defined by [runranges[i][0],runranges[i][1]] inclusive
    for (int j = runranges[i][0]; j < runranges[i][1] + 1; j++){
      skimfile.Form("%sskimDS%d_run%d_small.root" ,skim_folder.Data(), ds, j);
      skimCalib->Add(skimfile);
    }
  }//for loop

  // Turn off unnecessary branches
  skimCalib->SetBranchStatus("*", 0);

  vector<int>* channel = 0;
  skimCalib->SetBranchStatus("channel", 1);
  skimCalib->SetBranchAddress("channel", &channel);

  vector<double>* trapENFCal = 0;
  skimCalib->SetBranchStatus("trapENFCal", 1);
  skimCalib->SetBranchAddress("trapENFCal", &trapENFCal);

  vector<UInt_t>* wfDCBits = 0;
  skimCalib->SetBranchStatus("wfDCBits", 1);
  skimCalib->SetBranchAddress("wfDCBits", &wfDCBits);

  bool muVeto = 0;
  skimCalib->SetBranchStatus("muVeto", 1);
  skimCalib->SetBranchAddress("muVeto", &muVeto);

  bool isLNFill1 = 0;
  skimCalib->SetBranchStatus("isLNFill1", 1);
  skimCalib->SetBranchAddress("isLNFill1", &isLNFill1);

  bool isLNFill2 = 0;
  skimCalib->SetBranchStatus("isLNFill2", 1);
  skimCalib->SetBranchAddress("isLNFill2", &isLNFill2);

  vector<bool>* isGood = 0;
  skimCalib->SetBranchStatus("isGood", 1);
  skimCalib->SetBranchAddress("isGood", &isGood);

  vector<double>* avse = 0;
  skimCalib->SetBranchStatus("avse", 1);
  skimCalib->SetBranchAddress("avse", &avse);

  vector<double>* nlcblrwfSlope = 0;
  skimCalib->SetBranchStatus("nlcblrwfSlope", 1);
  skimCalib->SetBranchAddress("nlcblrwfSlope", &nlcblrwfSlope);

  vector<double>* dcr99 = 0;
  skimCalib->SetBranchStatus("dcr99", 1);
  skimCalib->SetBranchAddress("dcr99", &dcr99);

  vector<int>* mH = 0;
  skimCalib->SetBranchStatus("mH", 1);
  skimCalib->SetBranchAddress("mH", &mH);

  vector<int>* run = 0;
  skimCalib->SetBranchStatus("run",1);
  skimCalib->SetBranchAddress("run", &run);

  GATDataSet firstrun(runranges[0][0]);
  TString canvas_title, file_title, bigHistTitle, detPos;
  detPos = firstrun.GetChannelMap()->GetDetectorPos(chan);
  // skimHist Generation and Formatting
  gStyle->SetStatH(0.15);
  gStyle->SetStatY(0.4);
  bigHistTitle.Form("DCR 99 vs Run for Channel %d, %s", chan, detPos.Data());
  TH2D* bigSkimHist = new TH2D("bigSkimHist",bigHistTitle,500,runranges[0][0]-100,runranges[num_rows-1][0]+100,300,-0.003,0.001);

  skimCalib->Draw("dcr99:run>>bigSkimHist",cuts);
  bigSkimHist->GetXaxis()->SetTitle("Run");
  bigSkimHist->GetXaxis()->SetLabelSize(0.02);
  bigSkimHist->GetYaxis()->SetTitle("dcr99");
  bigSkimHist->GetYaxis()->SetLabelSize(0.02);
  bigSkimHist->GetYaxis()->SetTitleOffset(1.5);
  c1->Update();

  file_title.Form("%s(",packet_title.Data());
  canvas_title.Form("Title: DCR vs Run Number");
  c1->Print(file_title,canvas_title);
  c1->Clear();

  for(int i = 0; i < num_rows; i++){

    gStyle->SetStatY(0.9);
    TString skimHistTitle;
    skimHistTitle.Form("DCR 99, Channel %d, %s, Runs %d - %d", chan, detPos.Data(), runranges[i][0], runranges[i][1]);
    TH1D* skimHist = bigSkimHist->ProjectionY(skimHistTitle,bigSkimHist->GetXaxis()->FindBin(runranges[i][0]),bigSkimHist->GetXaxis()->FindBin(runranges[i][1]),"");

    skimHist->SetTitle(skimHistTitle);

    skimHist->GetXaxis()->SetTitle("DCR 99");
    skimHist->GetXaxis()->SetLabelSize(0.02);
    skimHist->GetXaxis()->SetTitleOffset(1.3);

    skimHist->GetYaxis()->SetTitle("Count");
    skimHist->GetYaxis()->SetTitleOffset(1.5);
    skimHist->GetYaxis()->SetLabelSize(0.03);

    skimHist->Draw(); 
    // Plot dcr, dcr vs energy?
    // Calculate efficiency
    double integ_total, integ_to_zero, dcr99_eff;
    int minbin, maxbin, zerobin;
    
    minbin = skimHist->FindBin(-0.003);
    maxbin = skimHist->FindBin(0.001);
    zerobin = skimHist->FindBin(0);
  
    integ_to_zero = skimHist->Integral(minbin, zerobin);
    integ_total = skimHist->Integral(minbin, maxbin);
  
    if(integ_total == 0) {dcr99_eff = 0;}
    else {dcr99_eff = integ_to_zero/integ_total;}
    efficiencies[i] = dcr99_eff;
  
    // Should add in a text box with the efficiency of the cal run
  
    // Draw line at 0 for reference
    TLine * vert = new TLine(0,0,0,skimHist->GetMaximum());
    vert->SetLineColor(2);
    vert->Draw();
    c1->Update();
  
    // Add plots to final pdf
    canvas_title.Form("Title: %s",skimHistTitle.Data());
    file_title.Form("%s",packet_title.Data());
    c1->Print(file_title,canvas_title);
  
    c1->Clear();
    delete skimHist;
  } //for loop

  // Plot efficiencies from the whole dataset
  TString eff_hist_title;
  file_title.Form("%s)",packet_title.Data());
  eff_hist_title.Form("Chan %d DCR 99 Efficiencies for DS%d",chan,ds);
  canvas_title.Form("Title: %s",eff_hist_title.Data());

  double runstarts[num_rows];

  for(int i = 0; i<num_rows; i++){
    runstarts[i] = runranges[i][0];
  }

  TGraph* eff_graph = new TGraph(num_rows,runstarts,efficiencies);
  eff_graph->SetName("eff_graph");
  eff_graph->SetTitle(eff_hist_title);

  // Efficiency Hist Formatting
  eff_graph->SetMarkerStyle(7);
  eff_graph->GetYaxis()->SetRangeUser(0,1.05);
  eff_graph->GetYaxis()->SetTitle("DCR 99 Efficiency");
  eff_graph->GetXaxis()->SetTitle("Starting Run of Calibration");
  eff_graph->Draw("AP");
  c1->Update();

  c1->Print(file_title,canvas_title);
  c1->Close();
  delete eff_graph;
  delete bigSkimHist;
  return 1;
} //PlotDCR

int main (int argc, char* argv[])
{
  if (argc <3){
    cout << "Usage: "<<argv[0]<<" 'dataset number' 'channel' 'gat_tag'"<<endl;
    return 1;
  }

  // Arguments should be dataset,channel,gat_tag in that order
  int i = 1;
  int dataset = atoi(argv[i++]);
  TString chan = argv[i++];
  int channel = atoi(chan);
  TString gat_tag = argv[i++];

  // Make sure they are in the right order
  if (dataset != 5 && dataset != 6){
    cout<< "Only datasets 5 and 6 are functional right now, use 5 or 6 when inputting the dataset."<<endl;
    cout<< "You input dataset " << dataset <<"."<<endl;
    return 1;
  }
  else if (channel < 500){
    cout<<"Please input at least a viable channel number." <<endl;
    cout<<"You input channel " << channel <<"."<<endl;
    return 1;
  }
  else { //Let's see if you did everything correctly
    if (dataset == 5 && chan.Length() == 3){ //M1
      vector< vector<unsigned int> > runBoundaries(6, vector<unsigned int>(2));
      runBoundaries =  {{24305,24318},{24539,24552},{24761,24775},{24971,24984},{25248,25261},{25479,25492}};
      return PlotDCR(channel, dataset, gat_tag, runBoundaries);
    }
    else if( dataset == 5 && chan.Length() == 4){ //M2
      vector< vector<unsigned int> > runBoundaries(7, vector<unsigned int>(2));
      runBoundaries = {{23960,23970},{24322,24332},{24556,24567},{24779,24789},{24988,24998},{25265,25275},{25496,25506}};
      return PlotDCR(channel, dataset, gat_tag, runBoundaries);
    }
    else if (dataset == 6 && chan.Length() == 3){ //M1
      vector< vector<unsigned int> > runBoundaries(43, vector<unsigned int>(43));
      runBoundaries = {{25690,25702},{25834,25935},{26042,26049},{26215,26236},{26381,26404},{26623,26646},{26750,26771},{26946,26967},{27180,27194},{27938,27951},{27975,27988},{28113,28133},{28322,28343},{28468,28608},{28970,28990},{29356,29376},{29525,29545},{29698,29718},{29915,29934},{30059,30077},{30328,30346},{31325,31343},{31685,31701},{31780,31791},{31919,31939},{32008,32015},{32024,32041},{32161,32178},{32416,32451},{32855,32884},{33060,33230},{33510,33526},{33654,33671},{33693,33710},{33910,33926},{34075,34091},{34271,34287},{34457,34471},{34501,34688},{34819,34835},{35031,35047},{35197,35215},{35366,35382}};
      return PlotDCR(channel, dataset, gat_tag, runBoundaries);
    }
    else if (dataset == 6 && chan.Length() == 4){ //M2
      vector< vector<unsigned int> > runBoundaries(43, vector<unsigned int>(43));
      runBoundaries = {{25676,25686},{25939,26020},{26042,26049},{26215,26236},{26381,26404},{26623,26646},{26750,26771},{26946,26967},{27180,27194},{27938,27951},{27975,27988},{28113,28133},{28322,28343},{28468,28608},{28970,28990},{29356,29376},{29525,29545},{29698,29718},{29915,29934},{30059,30077},{30328,30346},{31325,31343},{31685,31701},{31780,31791},{31919,31939},{32008,32015},{32024,32041},{32161,32178},{32416,32451},{32855,32884},{33060,33230},{33510,33526},{33654,33671},{33693,33710},{33910,33926},{34075,34091},{34271,34287},{34457,34471},{34501,34688},{34819,34835},{35031,35047},{35197,35215},{35366,35382}};
      return PlotDCR(channel, dataset, gat_tag, runBoundaries);
    }
    else { // I guess not :/ 
      cout <<"Something went wrong"<<endl;
      return 1;
    }
  }
}
