#!/usr/bin/env python3
import ROOT
import optparse
import numpy
import os, sys
import math
from array import array
import json, glob

year=sys.argv[1]
sampleList=sys.argv[2]
verbose=(len(sys.argv)==4)

for sample in sampleList.split(","):

    production = "Spring21ULYEARFS_106X_nAODv9_FullYEARv8".replace('YEAR', year).replace('UL20', 'UL')
    inputDir = "/eos/cms/store/group/phys_susy/Chargino/Nano/"+production+"/susyGen"
    finalDir = inputDir+"__FSSusyYEARv8__FSSusyCorrYEARv8__FSSusyNominYEARv8__susyMT2fastSmear".replace('YEAR', year)
    if "2016" in year:
        finalDir = finalDir.replace("FSSusyCorr2016v8__FSSusyNomin2016v8", "FSSusyCorr2016v8HIPM__FSSusyNomin2016v8HIPM")

    files = glob.glob(finalDir+"/nanoLatino_"+sample+"_ext1__part*.root")

    firstFile = True

    print("Processing", year, sample, "dataset with", str(len(files)), "final files")

    nInputFiles = 0

    for file in files:

        if verbose and nInputFiles>0 and nInputFiles%1000==0:
            print("   Reading file", nInputFiles)

        infile = ROOT.TFile.Open(inputDir+"/"+file.split("/")[-1],"read")

        pMSSMCount = infile.Get("pMSSMCount")

        if not pMSSMCount:
            print("pMSSMCount not found in", file) 
            continue
    
        if firstFile:
            totalCount = pMSSMCount
            nInputFiles += 1
            firstFile = False

        else: 
            totalCount.Add(pMSSMCount)
            nInputFiles += 1

    if not firstFile:
        print("totalCount =", totalCount.GetEntries(), "in", nInputFiles, "files")
        os.system("mkdir -p THnSparse/"+year+"/"+sample+"_ext1")
        outfile = ROOT.TFile.Open("THnSparse/"+year+"/"+sample+"_ext1/"+sample+"_ext1_"+year+"_Total_CR_mt2ll.root","recreate")
        outfile.cd()
        totalCount.Write()
        outfile.Close()


