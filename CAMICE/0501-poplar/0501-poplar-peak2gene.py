#!/usr/bin/env python2
import pymisca.header as pyhead
execfile(pyhead.base__file('headers/header__import.py'))
# HOST = pyhead.base__check('HOST')

CUTOFF_PEAK2GENE= 5000
# gconf = pyutil.readBaseFile('results/0219__prepareGCONF__Ath/gconf.npy').tolist()
gconf = pyutil.readBaseFile('results/0501-prepareGCONF-poplar/gconf.npy').tolist()

    
with pyext.FrozenPath(pyext.base__file()) as p:
    fnames = pyext.glob.glob('results/0501-poplar-chiptargpeak/output/*.bed',)
    
# fnames = [
# 'results/0224__chipTarg__CAMICE/output/CAMTA-CHX.bed',
#  'results/0224__chipTarg__CAMICE/output/CAMTA-cold.bed',
#  'results/0224__chipTarg__CAMICE/output/ICE1-CHX.bed',
#  'results/0224__chipTarg__CAMICE/output/ICE1-cold.bed',
# 'results/0224__chipTarg__CAMICE/output/CAMTA-CHX194.bed',
# ]

for fname in fnames:
    fname = pyext.base__file(fname)
    res = sdio.job__nearAUG(
        peakFile=fname,        
        featFile=gconf.GTF+'.cds',
        GSIZE=gconf.GSIZE,
        CUTOFF=CUTOFF_PEAK2GENE,
#         CUTOFF=3000,
    )
    pyutil.shellexec('mkdir -p output/')
    pyutil.file__link(res,'output/%s.%s'%(pyutil.getBname(fname),
                                         res.rsplit('.',1)[-1]),
                     force=True,)
    #     bed = pyutil.readBaseFile(fname,)
#     break
print ('[DONE]')