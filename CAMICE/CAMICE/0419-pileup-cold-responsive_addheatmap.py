#!/usr/bin/env python2
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
    figsize=[ 25, 20 ],
    show_axa = 1,
    showGrid=0,
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
    chipTks.keyDFTrack,
#     keyDF[['BioName']],
]    

cluFile= 'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0411_coldonly_ratio_outcsv/baseDist-vmfDistribution_seed-0/clu.csv'
pyext.localise(cluFile,baseFile=1)
# cluFile =     'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0411_coldonly_ratio_outcsv/baseDist-vmfDistribution_seed-0/cluc.csv'
# common = dict(order=order,)
clu = pyext.readBaseFile(cluFile)[['clu','score']].query('score > 2')
res = sjob.job__render__panelPlot(
    clu=clu,
    tracks = tracks,
    index=vdf.index & clu.index,
    panel_kw=panel_kw,
    aliasFmt = 'confident-targets-heatmap',
#     **common
)
figs.update([res])


clu = pyext.readBaseFile(cluFile)[['clu','score']].query('clu==0 & score > 2')
res = sjob.job__render__panelPlot(
    clu=clu,
    tracks = tracks,
    index=vdf.index & clu.index,
    panel_kw=panel_kw,
    aliasFmt = 'confident-targets-heatmap-CYHr1',
#     **common
)
figs.update([res])

job = lambda :pyutil.render__images(figs,exts=['png','svg'])
pyext.func__inDIR(job,DIR=pyext.base__file('results/0419-pileup-cold-responsive/heatmaps',
                                           force=1,asDIR=1))

# rnaTracks.__dict__.values()