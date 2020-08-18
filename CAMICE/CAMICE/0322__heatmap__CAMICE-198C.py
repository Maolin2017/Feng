#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymisca.header as pyhead
execfile(pyhead.base__file('headers/header__import.py'))
figs = pyutil.collections.OrderedDict()

keyDF = pyutil.readData('/home/feng/meta/key_ath.csv')

HOST = pyhead.base__check('HOST')

gconf = pyutil.readBaseFile('results/0219__prepareGCONF__Ath/gconf.npy').tolist()

#### Load Tracks
chipTks = pyutil.readBaseFile('results/0224__chipTracks__CAMICE/tracks.npy').tolist()

# url = 'http://172.26.114.34:81/static/figures/0122__prepareRNA__CAMICE/tracks.npy'
url = 'results/0224__prepareRNA__CAMICE/tracks.npy'
tks = rnaTks = rnaTracks = pyutil.readBaseFile(url).tolist()
for v in vars(rnaTks).values():
    v.height = 4.
    


panel_kw=dict(
    figsize=[ 20, 20 ],
    show_axa = 1
)

vdf = pd.concat([tks.cold_wt,
    tks.cold_mut,
    tks.chx_wt,
    tks.chx_mut,
    tks.chem_wt,],axis=1)

vdf = scount.countMatrix(vdf).qc_Avg()
pyvis.qc_2var(*vdf.summary[['per_MSQ','MSQ']].values.T)
indexVis = index = vdf.summary.query('per_MSQ > 0.6').index
figs['drange-cutoff'] = plt.gcf()

tracks = [
    'cluTrack', 
] + sorted(chipTks.__dict__.values(),key=lambda x:x.name) + [
    tks.cold_wt,
    tks.cold_mut,
    tks.chx_wt,
    tks.chx_mut,
    tks.chem_wt,
    chipTks.keyDFTrack
#     keyDF[['BioName']],
]    
# rnaTracks.__dict__.values()

cluFile = '/home/feng/work/results/0224__showCluster__CAMICE/clu.csv'
order =  cluFile = 'results/0322__cluster__CAMICE/clu.csv'
# order = cluFile = 'results/0408-cluster-CAMICE/0408-freezerCluster/results0407-prefiltering-camicetopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-1/clu.csv'
# cluFile = pyext.readBaseFile(cluFile)[['clu']]
common = dict(order=order,baseFile=1)
# dClu = pyutil.readBaseFile('/home/feng/work/results/0224__showCluster__CAMICE/cache.npy').tolist()


res = sjob.job__render__panelPlot(
    clu=cluFile,
    tracks = tracks,
#     order=dClu['stats'],
#     order=order,
    
    index=None,
    panel_kw=panel_kw,
    aliasFmt = 'allClustered',
    **common

)
figs.update([res])

res = sjob.job__render__panelPlot(
    clu=cluFile,
    tracks = tracks,
#     order=order,
    index=indexVis,
    panel_kw=panel_kw,
    aliasFmt = 'visualFiltered',
    **common
)
figs.update([res])

res = sjob.job__render__panelPlot(
    clu=cluFile,
    tracks = tracks,
#     order=dClu['stats'],
    index='indexVis & clu.query("clu==2").index',
    extra = dict(indexVis=indexVis),
    panel_kw=panel_kw,
    aliasFmt = 'visualFiltered-clu2',
    **common
)
figs.update([res])


res = sjob.job__render__panelPlot(
    clu=cluFile,
    tracks = tracks,
#     order=dClu['stats'],
#     order=order,
    index='indexVis & chipTks["ICE1-CHX"].index',
    extra = dict(indexVis=indexVis,chipTks=chipTks),
    panel_kw=panel_kw,
    aliasFmt = 'visualFiltered-ICE1-CHX',
    **common

)
figs.update([res])





# keyDFC = dClu['stats'].merge(keyDF,left_index=True,right_index=True)
# keyDFC.to_html('keyDFC.html')
# keyDFC.to_csv('keyDFC.csv')

# pyutil.render__images(figs)

pyutil.render__images(figs,exts=['png',])