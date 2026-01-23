#!/usr/bin/env python3
import ROOT
import optparse
import numpy
import os, sys
import math
from array import array
import json, glob

year=sys.argv[1]
sample=sys.argv[2]
verbose=(len(sys.argv)==4)

production = "Spring21ULYEARFS_106X_nAODv9_FullYEARv8".replace('YEAR', sys.argv[1]).replace('UL20', 'UL').replace('noHIPM','').replace('HIPM','')
inputDir = "/eos/cms/store/group/phys_susy/Chargino/Nano/"+production+"/susyGen/"
mainLogDir   = "/afs/cern.ch/work/s/scodella/SUSY/logs28/jobs/NanoGardening__"+production+"__susyGen/"+sample

files = glob.glob(inputDir+"nanoLatino_"+sys.argv[2]+"__part*.root")

pMSSMModelCount = {}

for file in files:
    
    filepart = file.split("__part")[-1].replace(".root","")
    subDir = "/sub"+str(int(int(filepart)/1000))
    logfilename = mainLogDir + subDir+"/NanoGardening__"+production+"__susyGen__"+sample+"__part"+filepart+".out"

    if not os.path.isfile(logfilename): 
        print("Error: log file", logfilename, "not found!")
        exit()

    if verbose: print("Reading", logfilename)

    with open(logfilename, "r") as logfile:

        totalCount, totalProcessed, modelTotalCounting = -1, -1, 0
        modelWithMissingCounting = []

        for line in logfile:
            sline = line.strip()
            if "Finally selected" in sline and "Processed" in sline:
                if "Adding file" not in sline:
                    totalProcessed = int(sline.split(" ")[1])
            elif "totalCount" in sline:
                if "Adding file" not in sline:
                    totalCount = int(sline.split(" ")[-1])
            elif "[id1" in sline and "id2" in sline and "]" in sline:
                modelName = sline.split("[")[1].split("]")[0]
                if "Adding file" not in sline:
                    if modelName not in pMSSMModelCount:
                        pMSSMModelCount[modelName] = 0
                    pMSSMModelCount[modelName] += int(sline.split(" ")[-1])
                    modelTotalCounting += int(sline.split(" ")[-1])
                else:
                    modelWithMissingCounting.append(modelName)

        if totalCount==-1 and totalProcessed==-1:
            print("Error: no valid info on total event counting")
            exit()

        if totalCount!=-1 and totalProcessed!=-1 and totalCount!=totalProcessed:
            print("Error: inconsistent info on total event counting")
            exit()

        if totalCount==-1: totalCount = totalProcessed

        if len(modelWithMissingCounting)>1: 
            print("Error:", modelWithMissingCounting, "models with missing counting")
            exit()
        elif len(modelWithMissingCounting)==1:
            pMSSMModelCount[modelWithMissingCounting[0]] = totalCount - modelTotalCounting
        elif modelTotalCounting!=totalCount:
            print("Error: total counting from models inconsistent with total counting in", logfilename, modelTotalCounting, totalCount)
            #exit()






