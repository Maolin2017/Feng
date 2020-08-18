#!/usr/bin/env python2
import pymisca.header as pyheader
pyheader.base__check()
pyheader.execBaseFile('headers/header__import.py')
figs = pyext.collections.OrderedDict()

# pyutil.envSource('')
mcurr = pyext.readBaseFile('upGeo-results/0407-database-mapped/mcurr.csv',guess_index=0)
rnaCurr = pyext.readBaseFile('meta/src/0424-rnacurr-poplar-dapseq.tsv')
mcurr = mcurr.query('DATAACC in @rnaCurr.index')
rnaCurr['npkFile'] = mcurr.query('EXT=="narrowPeak"').set_index('DATAACC')['FULL_PATH']
rnaCurr['RPKMFile'] = mcurr.query('BASENAME.str.endswith("RPKM.bw")').set_index('DATAACC')['FULL_PATH']

rnaCurr['header'] = rnaCurr['bname']

# treatment = '174CS24'
# with pyext.FrozenPath()

res = sjob.job__chipTargPaired(
    CUTOFF_FC=6,
    treatment='174CS24',
    control='174CS20',
    bwMeta=rnaCurr,
#     name='174CS24-FC3'
)
figs.update(res[0])

res = sjob.job__chipTargPaired(
    CUTOFF_FC=6,
    treatment='166CS24',
    control='174CS20',
    bwMeta=rnaCurr,
#     name = '166CS24-FC3'
#     name='PIF-chip',
)
figs.update(res[0])


pyutil.render__images(figs,)

# res[1].to_csv('clu.csv')