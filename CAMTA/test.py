# reload(sdio)
execfile('/home/feng/meta/header_0903.py')
execfile('/home/feng/meta/header__script2figure.py')
# bwMeta 
import synotil.chipShot as mod ;reload(mod)
bwCurr = bwMeta.query('runID=="182C"').query('bamFinal.str.contains("TAIR10")')
bwFlat = ' '.join(bwCurr.RPKMFile)
bedFile = '/home/feng/meta/key_ath.csv.cds.summit'
GTF = '/home/feng/ref/Arabidopsis_thaliana_TAIR10/annotation/genes.gtf'
GSIZE='/home/feng/ref/Arabidopsis_thaliana_TAIR10/genome.sizes'
# import
mod.main(bedFile=bedFile,
         bwFiles=bwCurr.fname,
          gtfFile=GTF,
    center_summit=1,
NCORE=6,
radius=6000,debug=0,
         GSIZE= GSIZE,
)
# ! chipShot.py -r 6000 -s1 -j6 -d0 -a {GTF} -b {bedFile}  {bwFlat} 