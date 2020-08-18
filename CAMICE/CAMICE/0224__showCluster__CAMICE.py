#!/usr/bin/env python
import pymisca.header as pyhead
execfile(pyhead.base__file('headers/header__import.py'))
figs = pyutil.collections.OrderedDict()


# reload(spanel)


import pymisca.model_collection.mixture_vmf as mod
# ti = 250
STEP = 330
CUTOFF_ENT=3.5

# url = 'http://172.26.114.34:81/static/figures/0122__prepareRNA__CAMICE/tracks.npy'

tks = rnaTracks = pyutil.readBaseFile('results/0224__prepareRNA__CAMICE/tracks.npy').tolist()
tdf = rnaTracks.cold_wt
tdf.vlim = [-2,2]

#### Get clu from model
fname = 'http://172.26.114.34:81/static/figures/0122__cluster__CAMICE-cold-mock/mdl.npy'
mdl0 = mdl = pyutil.readData(fname).tolist()

mod.qc__vmf(mdl,XCUT=STEP,YCUT=CUTOFF_ENT)
figs['qcVMF'] = plt.gcf()



# pyvis.abline(x0=ti)
mdl = mdl0.callback.mdls[STEP][-1]
mdl.predictClu = funcy.partial(
    mdl.predictClu,
    entropy_cutoff = CUTOFF_ENT,
    method='reorder',
)
tdf = scount.countMatrix(mdl0.data)

d = pyutil.cache__model4data(
    mdl,
    tdf=tdf)
d = pyutil.util_obj(**d)
np.save('cache.npy',d)

clu = d.clu
clu.to_csv('clu.csv')
spanel.panelPlot([clu,tdf]).render(order=d.stats, 
                                   figsize=[len(tdf)/1000.,len(tdf.T)/2.])
figs['heatmap'] = plt.gcf()

pyutil.render__images(figs)