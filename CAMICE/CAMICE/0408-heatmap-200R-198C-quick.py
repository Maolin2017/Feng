#!/usr/bin/env python2
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
    figsize=[ 25, 20 ],
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

# cluFile = '/home/feng/work/results/0224__showCluster__CAMICE/clu.csv'
# order =  cluFile = 'results/0322__cluster__CAMICE/clu.csv'
# order = cluFile = 'results/0408-cluster-CAMICE/0408-freezerCluster/results0407-prefiltering-camicetopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-1/cluc.csv'
# # cluFile = pyext.readBaseFile(cluFile)[['clu']]
# common = dict(order=order,baseFile=1)

# order = cluFile = 'results/0408-cluster-CAMICE/0408-freezerCluster/results0407-prefiltering-camicetopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-1/cluc.csv'
order = cluFile = 'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0409topped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/cluc.csv'
# results0407-prefiltering-camicetopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-1/cluc.csv'
# cluFile = pyext.readBaseFile(cluFile)[['clu']]
def makeJob(cluFile):
    clu = pyext.readBaseFile(cluFile)[['clu','score']]
    order = clu
    common = dict(order=order,baseFile=1)
    figs = pyext.collections.OrderedDict()
    # dClu = pyutil.readBaseFile('/home/feng/work/results/0224__showCluster__CAMICE/cache.npy').tolist()
    def job():
        res = sjob.job__render__panelPlot(
            clu=clu,
            tracks = tracks,

            index=vdf.index & clu.index,
            panel_kw=panel_kw,
            aliasFmt = 'confident-targets',
            **common
        )
        figs.update([res])


        pyutil.render__images(figs)
    return job

lst  = [
#     'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0409topped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/cluc.csv',
#     'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0409topped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/clu.csv',
#     'results/0408-cluster-CAMICE/0408-freezerCluster/results0408-prefiltering-camicetopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/clu.csv',
#     'results/0408-cluster-CAMICE/0408-freezerCluster/results0408-prefiltering-camicetopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/cluc.csv',
#     'results/0408-cluster-CAMICE/0408-freezerCluster/results0408-prefiltering-camicetopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/span90-clu.csv',
#     'results/0408-cluster-CAMICE/0408-freezerCluster/results0408-prefiltering-camicetopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/head350-clu.csv',
#     'results/0408-cluster-CAMICE/0408-freezerCluster/results0408-prefiltering-camicetopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/head600-clu.csv',
#     'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0409topped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/clu.csv'

#     'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0409topped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/head300-clu.csv',
#     'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0409topped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/head600-clu.csv',
#     'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0409topped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/span90-clu.csv',
    
#     'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0411_coldonlytopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/cluc.csv',
#     'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0411_coldonlytopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-1/cluc.csv',
#     'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0411_coldonlytopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-2/cluc.csv',
    
    'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0411_coldonly_ratio_outcsv/baseDist-vmfDistribution_seed-0/cluc.csv',
    'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0411_coldonly_ratio_outcsv/baseDist-vmfDistribution_seed-1/cluc.csv',
    'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0411_coldonly_ratio_outcsv/baseDist-vmfDistribution_seed-2/cluc.csv',
    
]
# http://172.26.114.34:81/static/results/0408-heatmap-200R-198C-quick/0408-prefiltering-camicedataset_0411_coldonlytopped-20-nmsd-meannormpkbasedist-vmfdistribution_seed-0cluccsv/figure.html
for cluFile in lst:
    pyext.func__inDIR( makeJob(cluFile),
                      slugify.slugify(unicode(pyext.splitPath(cluFile,level=3)[1]))

                     )