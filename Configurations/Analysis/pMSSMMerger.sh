#!/bin/bash

refstep=susyGen__susyW
treedir=/eos/cms/store/group/phys_susy/Chargino/Nano
year=${1//noHIPM/}
year=${year//HIPM/}
count=$(find $treedir/Spring21UL*_Full${year}v8/$refstep/nanoLatino_$2__part*.root -maxdepth 1 -type f | wc -l)

inputfile=./THnSparse/$1/$2/split/$2_$1
if [[ $3 == "sr" ]]; then
    inputfile=${inputfile}_SR
    if [[ $4 != "no" ]]; then
        inputfile=${inputfile}_CR
    fi
    if [[ $5 != "no" ]]; then
        inputfile=${inputfile}_mt2ll
    fi
else
    inputfile=${inputfile}_Total
fi

rootcount=$(find ${inputfile}_part*.root -maxdepth 1 -type f | wc -l)
if [[ "$count" == "$rootcount" ]]; then
	#../../../LatinoAnalysis/Tools/scripts/haddfast --compress $inputfile.root ${inputfile}_part*.root
	hadd -f $inputfile.root ${inputfile}_part*.root
        minimumsize=1000
        actualsize=$(wc -c <"$inputfile.root")
        if [ $actualsize -ge $minimumsize ]; then
	    outputFile=${inputfile//split/}
            mv $inputfile.root $outputFile.root
        fi
else
	echo The number of input files \($rootcount\) does not match the number of input trees \($count\)
fi



