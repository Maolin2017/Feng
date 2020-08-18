source /home/feng/envs/pipe/bin/activate

### Download test Data
bash test__data.sh

### Configure $GSIZE and .../genome.fa
source config_Ath_TAIR10.sh
export CDS=/home/feng/ref/Arabidopsis_thaliana_TAIR10/Annotation/genes.gtf.cds

### Run pipeline
pipeline_macs2.sh test.bam -c test__input.bam

####### OP1: per-chip operation
### find peaks near a promoter using .gtf.cds
### Help: filterByCDS.py -h
filterByCDS.py test_peaks.narrowPeak -g $GSIZE -c $CDS

### Using pandas for now, potentially reimplement using 'bedtools groupby'
firstByKey.py type\=closest_bed\=test_peaks_radius\=1_feat\=genes.gtf.cds.tsv


####### OP2: write a summary html
### taking multiple .narrowPeak if desired
### Help: chipSummary.py -h
chipSummary.py --ref $CDS test_peaks.narrowPeak

