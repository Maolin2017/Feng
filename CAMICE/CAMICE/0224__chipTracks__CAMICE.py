#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymisca.header as pyhead
execfile(pyhead.base__file('headers/header__import.py'))
figs = pyutil.collections.OrderedDict()

keyDF = pyutil.readData('/home/feng/meta/key_ath.csv')

HOST = pyhead.base__check('HOST')

# CUTOFF_PEAK2GENE=3000
gconf = pyutil.readBaseFile('results/0219__prepareGCONF__Ath/gconf.npy').tolist()
gid = sdio.extract_peak(gconf.GTF+'.cds').acc

with pyext.FrozenPath(pyext.base__file()) as p:
    fnames = pyext.glob.glob('results/*__peak2gene__*/output/*.tsv',)

# nMax = 500
nMax=1000
# fnames = [
#  'results/0224__peak2gene__CAMICE/output/CAMTA-CHX.tsv',
#  'results/0224__peak2gene__CAMICE/output/CAMTA-cold.tsv',
#  'results/0224__peak2gene__CAMICE/output/ICE1-CHX.tsv',
#  'results/0224__peak2gene__CAMICE/output/ICE1-cold.tsv',
#  'results/0224__peak2gene__CAMICE/output/CAMTA-CHX194.tsv',
# ]

lst =[]
for fname in fnames:
    name = pyutil.getBname(fname)
    dfc = pyutil.readBaseFile(fname)
    #### img = CHIPDIFF since img is the last column of synotil.dio.bedHeader
    if 'img' not in dfc.keys():
        print ('[]missing last column:%s'%fname)
    else:
        dfc = dfc.sort_values('img',ascending=False)
    index = dfc.feat_acc.drop_duplicates().values[:nMax]
    track = pyext.index2frame(index)
    track = scount.countMatrix(track,name=name)
#     .reindex(gid).fillna(False)
    lst += [(name,track)]
    print (name,track.shape)
    
res = dict(lst)
spanel.panelPlot(res.values()).render()



tks = pyutil.util_obj(**res)

fname = 'metaio/simpleModel/Tag/csv-markerGene-CAMICE'
res = pyutil.readBaseFile(fname,ext='json', baseFile=HOST)
res = pyutil.read__buffer(res['fields']['text'],ext='csv')
res =scount.countMatrix(res,name=pyutil.getBname(fname))
tks['keyDFTrack'] = res

np.save('tracks.npy',tks)

figs['qcMap'] = plt.gcf()
pyutil.render__images(figs)
    