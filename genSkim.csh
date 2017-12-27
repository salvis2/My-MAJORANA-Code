#!/bin/csh

source ~/.cshrc.ext
~/GAT/Apps/skim_mjd_data -s -f $1 > ../Logs/genCalibSkim_$1.log
