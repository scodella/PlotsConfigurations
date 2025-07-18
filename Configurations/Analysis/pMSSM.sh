#!/bin/bash
export X509_USER_PROXY=/afs/cern.ch/user/s/scodella/.proxy
voms-proxy-info
export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source $VO_CMS_SW_DIR/cmsset_default.sh
export CMSSWDIR=/afs/cern.ch/work/s/scodella/SUSY/CMSSW_13_3_1/
cd $CMSSWDIR
eval `scramv1 ru -sh`
ulimit -c 0

cd $TMPDIR
pwd

outputFileLocal=THnSparse/YEAR/SAMPLE/split/SAMPLE_YEARTOTALNAMECRNAMEMTLLNAME_partPART.root
outputFile=$CMSSWDIR/src/PlotsConfigurations/Configurations/Analysis/$outputFileLocal
if [ -f "$outputFile" ]; then
    echo The output file already exists.
else
    echo Producing THnSparse for YEAR, SAMPLE, partPART, ISTOTAL, ISCR ISMTLL.
    python3 $CMSSWDIR/src/PlotsConfigurations/Configurations/Analysis/pMSSM.py --year=YEAR --sample=SAMPLE --job=PART ISTOTAL ISCR ISMTLL 
    minimumsize=MINSIZE
    actualsize=$(wc -c <"$outputFileLocal")
    if [ $actualsize -ge $minimumsize ]; then
        mv $outputFileLocal $outputFile
    fi
fi



