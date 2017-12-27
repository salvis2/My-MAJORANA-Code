#!/bin/csh
# This file runs skim file generations on a single run number

source ~/.cshrc.ext
~/GAT/Apps/skim_mjd_data -s -f $1 > ../Logs/genCalibSkim_$1.log
