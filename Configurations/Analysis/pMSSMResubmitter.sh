#!/bin/bash

refstep=susyGen
treedir=/eos/cms/store/group/phys_susy/Chargino/Nano
year=${1//noHIPM/}
year=${year//HIPM/}

count=$(find $treedir/Spring21UL*_Full${year}v8/$refstep/nanoLatino_$2__part*.root -maxdepth 1 -type f | wc -l)
if [[ "$count" -gt 5000 ]]; then
    count=5000
fi

mkdir -p condor/${1}/$2/split
logdir=condor/${1}/$2/split

outputfile=./THnSparse/$1/$2/split/$2_$1
if [[ $3 == "sr" ]]; then
    outputfile=${outputfile}_SR
elif [[ $3 == "full" ]]; then
    outputfile=${outputfile}_Full
else
    outputfile=${outputfile}_Total
fi
if [[ $4 != "no" ]]; then
    outputfile=${outputfile}_CR
fi
if [[ $5 != "no" ]]; then
    outputfile=${outputfile}_mt2ll
fi
if [[ $6 != "no" ]]; then
    outputfile=${outputfile}_noweight
fi
outputfile=${outputfile}_part

rootcount=$(find ${outputfile}*.root -maxdepth 1 -type f | wc -l)
if [[ "$count" == "$rootcount" ]]; then
    echo Output file found for all $count trees in $refstep
else
    let "missingfiles = count - rootcount"
    echo Missing $missingfiles output files out of $count trees in $refstep
fi

let "count = count - 1"
joblist=()
hasjobs=false
for i in $(seq 0 $count); do 

    doThisPart=true

    outputFile=$outputfile$i.root
    if [ -f "$outputFile" ]; then
        minimumsize=1000
        actualsize=$(wc -c <"$outputFile")
        if [ $actualsize -ge $minimumsize ]; then
            doThisPart=false
	fi
    fi

    logfile=condor/${1}/${2}/split/pMSSM_$3_$4_$5_$6.$i.log
    if [ -f "$logfile" ]; then
        doThisPart=false
    fi

    if [ "$doThisPart" = true ]; then
	hasjobs=true
        joblist+=("$i")
    fi

done

if [ "$hasjobs" = true ]; then

    shfilelocal=pMSSM_$3_$4_$5_$6
    shfile=$logdir/$shfilelocal
    cp pMSSM.sh $shfile.sh
    #cp pMSSM.py $logdir/
    cp pMSSM.py /eos/user/s/scodella/SUSY/pMSSM/

    sed -i 's/YEAR/'${1}'/g'   $shfile.sh
    sed -i 's/SAMPLE/'${2}'/g' $shfile.sh
    sed -i 's/PART/\$1/g'      $shfile.sh
    sed -i 's/MINSIZE/1000/g'      $shfile.sh

    if [[ $3 == "full" ]]; then
        sed -i 's/TOTALNAME/_Full/g' $shfile.sh
        sed -i 's/ISTOTAL/--level=full/g'      $shfile.sh
    elif [[ $3 == "sr" ]]; then
        sed -i 's/TOTALNAME/_SR/g' $shfile.sh
        sed -i 's/ISTOTAL/--level=sr/g'      $shfile.sh
    else
        sed -i 's/TOTALNAME/_Total/g' $shfile.sh
        sed -i 's/ISTOTAL/--level=total/g'  $shfile.sh
    fi        

    if [[ $4 == "no" ]]; then
        sed -i 's/CRNAME//g' $shfile.sh
        sed -i 's/ISCR//g'      $shfile.sh
    else
        sed -i 's/CRNAME/_CR/g' $shfile.sh
        sed -i 's/ISCR/--addcr/g'  $shfile.sh
    fi

    if [[ $5 == "no" ]]; then
        sed -i 's/MTLLNAME//g' $shfile.sh
        sed -i 's/ISMTLL//g'      $shfile.sh
    else
        sed -i 's/MTLLNAME/_mt2ll/g' $shfile.sh
        sed -i 's/ISMTLL/--splitmtll/g'  $shfile.sh
    fi

    if [[ $6 == "no" ]]; then
        sed -i 's/WEIGHTNAME//g' $shfile.sh
        sed -i 's/ISNOWEIGHT//g'      $shfile.sh
    else
        sed -i 's/WEIGHTNAME/_noweight/g' $shfile.sh
        sed -i 's/ISNOWEIGHT/--noweight/g'  $shfile.sh
    fi

    chmod a+x $shfile.sh

    echo executable            = $PWD/$shfile.sh               >  $shfile.sub
    echo arguments             = \$\(JOBNUM\)                  >> $shfile.sub
    #echo should_transfer_files = YES                           >> $shfile.sub
    #echo transfer_input_files  = $PWD/$logdir/pMSSM.py         >> $shfile.sub
    echo output                = $PWD/$shfile.\$\(JOBNUM\).out >> $shfile.sub
    echo error                 = $PWD/$shfile.\$\(JOBNUM\).err >> $shfile.sub
    echo log                   = $PWD/$shfile.\$\(JOBNUM\).log >> $shfile.sub
    echo +JobFlavour           = \"testmatch\"                 >> $shfile.sub
    #echo queue 1 input in $joblist                             >> $shfile.sub
    echo queue JOBNUM from \(                               >> $shfile.sub 
    for i in "${!joblist[@]}"; do
        echo "                       ${joblist[$i]}" >> $shfile.sub
    done
    echo \)                                       >> $shfile.sub

    cd $logdir/
    condor_submit $shfilelocal.sub
    cd ..

else
    echo "No jobs to resubmit"
fi


