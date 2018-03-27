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

int DCR2dplotter(){
  
  int channels[5] = {690,1174,1204,1302,1332};
  TString skim_folder, dest_folder, cuts, skim_files;
  
  dest_folder.Form("/global/projecta/projectdirs/majorana/users/salvis/analysis/DCR/quality/plots/DS6/dcr99/");
  skim_folder.Form("/global/project/projectdirs/majorana/data/mjd/surfmjd/analysis/skim/DS6cal/GAT-v01-07-253-gd5e677e/");
  skim_files.Form("%s*.root",skim_folder.Data());

  TChain* skimCalib = new TChain("skimTree");
  skimCalib->Add(skim_files);

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

  TCanvas* c1 = new TCanvas("c1","c1",600,600);

  // Set Up Channel Map for Plots
  GATDataSet ds(30059);
  TString detPos;

  for (int i = 0; i < 5; i++){
    int chan = channels[i];
    cuts.Form("isGood && trapENFCal > 1000 && trapENFCal < 2380 && !wfDCBits && !muVeto && mH == 1  && avse > -1 && !isLNFill1 && !isLNFill2 && channel == %d", chan);

    detPos = ds.GetChannelMap()->GetDetectorPos(chan);
    TString hist_title, file_title;
    file_title.Form("%sdcr99_vs_E_chan%d.pdf",dest_folder.Data(),chan);
    hist_title.Form("DCR 99 vs trapENFCal vs Run for Ch %d, %s",chan,detPos.Data());

    TH2D* dcr_hist = new TH2D("dcr_hist",hist_title,500,1000,2380,300,-0.0015,0.0015);

    skimCalib->Draw("dcr99:trapENFCal:run>>dcr_hist",cuts,"COLZ"); 

    // Hist Formatting
    dcr_hist->GetXaxis()->SetTitle("trapENFCal");
    dcr_hist->GetXaxis()->SetLabelSize(0.02);
    dcr_hist->GetYaxis()->SetTitle("dcr99");
    dcr_hist->GetYaxis()->SetLabelSize(0.02);
    dcr_hist->GetYaxis()->SetTitleOffset(1.5);
    dcr_hist->SetTitle(hist_title);
    dcr_hist->SetStats(false);
    dcr_hist->GetZaxis()->SetLabelSize(0.02);
    dcr_hist->GetZaxis()->SetTitle("run");

    c1->Update();
    c1->SaveAs(file_title);
    
    delete dcr_hist;
    c1->Clear();
  }
  return 1;
}
int main(int argc, char* argv[]){
  return DCR2dplotter();
}
