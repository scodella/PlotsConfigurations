#!/bin/bash

refstep=susyGen
treedir=/eos/cms/store/group/phys_susy/Chargino/Nano
year=${1//noHIPM/}
year=${year//HIPM/}

count=$(find $treedir/Spring21UL*_Full${year}v8/$refstep/nanoLatino_$2__part*.root -maxdepth 1 -type f | wc -l)

if [[ "$count" -gt 5000 ]]; then
    count=5000
fi

echo "Input files should be" $count

inputfile=./THnSparse/$1/$2/split/$2_$1
if [[ $3 == "sr" ]]; then
    inputfile=${inputfile}_SR
elif [[ $3 == "full" ]]; then
    inputfile=${inputfile}_Full
else
    inputfile=${inputfile}_Total
fi
if [[ $4 != "no" ]]; then
    inputfile=${inputfile}_CR
fi
if [[ $5 != "no" ]]; then
    inputfile=${inputfile}_mt2ll
fi
if [[ $6 != "no" ]]; then
    inputfile=${inputfile}_noweight
fi

maxfiles=500
minimumsize=1000

rootcount=$(find ${inputfile}_part*.root -maxdepth 1 -type f | wc -l)

echo "Found " $rootcount "input files"

if [[ "$count" == "$rootcount" ]]; then
    if [ $rootcount -ge $maxfiles ]; then
	filelist=""
	mergepart=0
	for job in $(seq 1 $rootcount) ; do
	    let "part=job-1"
	    filelist+=" "${inputfile}_part$part.root
	    let "mod=job%maxfiles"
	    if [[ $mod -eq "0" ]] || [[ $job -eq $rootcount ]] ; then
		partialfiletmp=${inputfile}_tmp_mergepart${mergepart}.root
	        hadd -f $partialfiletmp $filelist
		actualsize=$(wc -c <"$partialfiletmp")
		if [ $actualsize -ge $minimumsize ]; then
	            partialfile=${partialfiletmp//_tmp/}
		    mv $partialfiletmp $partialfile
		fi
		filelist=""
		let "mergepart=mergepart+1"
	    fi
	done
	partialfilelist=""
	for part in $(seq 1 $mergepart) ; do
	    let "rpart=part-1"
	    partialfilelist+=" "${inputfile}_mergepart${rpart}.root
	done
        hadd -f $inputfile.root $partialfilelist
        rm $partialfilelist	
    else
	#../../../LatinoAnalysis/Tools/scripts/haddfast --compress $inputfile.root ${inputfile}_part*.root
	hadd -f $inputfile.root ${inputfile}_part*.root
    fi
    actualsize=$(wc -c <"$inputfile.root")
    if [ $actualsize -ge $minimumsize ]; then
	outputFile=${inputfile//split/}
        mv $inputfile.root $outputFile.root
    fi
else
	echo The number of input files \($rootcount\) does not match the number of input trees \($count\)
fi



