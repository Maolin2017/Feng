#!/usr/bin/env python2
import pymisca.header as pyhead
execfile(pyhead.base__file('headers/header__import.py'))
# HOST = pyhead.base__check('HOST')
import os

gconf = pyutil.readBaseFile('results/0501-prepareGCONF-poplar/gconf.npy').tolist()
# gconf.GTF
peak2geneFile = fname = 'results/0501-poplar-peak2gene/output/174CS20-166CS24.tsv'
pyext.shellexec('mkdir -p output')
def worker(fname):
    BNAME = pyext.getBname(fname)
    peak2gene = pyext.readBaseFile(fname)
    dfc = peak2gene.merge(gconf.defline,right_index=True,left_on='feat_acc')
    # dfc.query('@dfc["Best-hit-arabi-name"].str.contains("AT1G01060")')
    # COLS = ['chrom','start','end','acc','score','strand','FC',]
    dfc = dfc.drop(columns =['img',])
    sutil.to_tsv(dfc,'output/{BNAME}-all-fileterpeak-withdefline.csv'.format(**locals()),index=0)

    dfc = dfc.sort_values(['feat_acc','FC'],ascending=False).groupby('feat_acc').first()
    sutil.to_tsv(dfc,'output/{BNAME}-best-filterpeak-withdefline.csv'.format(**locals()),index=0)

map(worker,pyext.glob.glob(os.path.join(pyext.base__file(),
                                        'results/0501-poplar-peak2gene/output/*.tsv')))