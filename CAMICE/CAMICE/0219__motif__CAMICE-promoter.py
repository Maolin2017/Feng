#!/bin/bash
# -*- coding: utf-8 -*-
RAD=0
export PATH=/home/feng/local/bin:$PATH    
. /home/feng/.bash_profile
. /home/feng/envs/pipe/bin/activate
. config_Ath_TAIR10.sh
echo [test]`which meme`
# export DB_MOTIF="/home/feng/ref/motif/ARABD/ArabidopsisPBM_20140210.meme"


# "http://172.26.114.34:81/static/figures/1219__ELF3__diffBind__summitDist/greped__merged__1219__ELF3__diffbind_radius=500.tsv" \

# "http://172.26.114.34:81/static/lists/0108__polyQ__funcPeak.bed.summit"
# "http://172.26.114.34:81/static/lists/0110__polyQ.bed.summit"
# "http://172.26.114.34:81/static/lists/0111__polyQ.bed.summit"
DB_MOTIF="
/home/feng/ref/motif/CIS-BP/Arabidopsis_thaliana.meme
/home/feng/ref/motif/JASPAR/JASPAR2018_CORE_plants_non-redundant.meme
/home/feng/ref/motif/ARABD/ArabidopsisPBM_20140210.meme
"
export DB_MOTIF=`echo "$DB_MOTIF"`


for URL in \
"http://172.26.114.34:81/static/results/0219__callRNATarget__CAMICE/chx-responsive-promoter.bed"
do
wget -N "$URL"
INFILE=`basename $URL`
OFILE=$INFILE.r$RAD.bed
bedtools slop -i $INFILE -g $GSIZE -b $RAD  \
| bedtools sort | bedtools merge \
>$OFILE
# ln -f functionalPeaks.narrowPeak functionalPeaks.bed
INFILE=$OFILE
quickFasta $INFILE
pipeline_motif.sh $INFILE
done