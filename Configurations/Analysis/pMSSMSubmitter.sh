#!/bin/bash

refstep=susyGen__susyW
treedir=/eos/cms/store/group/phys_susy/Chargino/Nano
year=${1//noHIPM/}
year=${year//HIPM/}
count=$(find $treedir/Spring21UL*_Full${year}v8/$refstep/nanoLatino_$2__part*.root -maxdepth 1 -type f | wc -l)

mkdir -p condor/${1}/$2/split/
logdir=condor/${1}/$2/split/

mkdir -p ./THnSparse/${1}/$2/split/

shfile=$logdir/pMSSM_$3_$4_$5_$6
cp pMSSM.sh $shfile.sh

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
echo arguments             = \$\(ProcId\)                  >> $shfile.sub
echo output                = $PWD/$shfile.\$\(ProcId\).out >> $shfile.sub
echo error                 = $PWD/$shfile.\$\(ProcId\).err >> $shfile.sub
echo log                   = $PWD/$shfile.\$\(ProcId\).log >> $shfile.sub
echo +JobFlavour           = \"longlunch\"                 >> $shfile.sub
echo queue $count                                          >> $shfile.sub

condor_submit $shfile.sub

