#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymisca.header as pyhead
execfile(pyhead.base__file('headers/header__import.py'))
figs = pyutil.collections.OrderedDict()

chipTks = pyutil.readBaseFile('results/0224__chipTracks__CAMICE/tracks.npy').tolist()
url = 'results/0224__prepareRNA__CAMICE/tracks.npy'
tks = rnaTks = rnaTracks = pyutil.readBaseFile(url).tolist()
bkdIndex = rnaTks.rnaDF.index
# chipTks['198C-CAMTA1-camta123-CHX-R2']
ax = plt.gca()
def plotter(xlab,ylab,ax=None):
#     if ax is None
#         ax = plt.gca()
#     xlab = 'CAMTA-CHX194'
#     ylab =  'ICE1-CHX'
    left = chipTks[xlab] 
    right = chipTks[ylab]
    indDF,ax = pyvis.qc_index(left.index,right.index,silent=0,
                              ax=ax,xlab=xlab,ylab=ylab);
    return indDF,ax
kit,it = zip(*chipTks.__dict__.items())
# %pdb 0
res = pyutil.mapper_2d(wFunc=lambda x,y: 
                       pymisca.proba.index__getFisher(x.index,y.index,bkdIndex=bkdIndex)['p'],
                           xs= it,ys=it)


np.fill_diagonal(res,np.nan)
res = pd.DataFrame(res,columns=kit,index=kit)
res = res.apply(lambda x:-np.log2(x))
res = res.fillna(0.)
res =scount.countMatrix(res)
toDrop = ['keyDFTrack']
res = res.drop(index=toDrop,columns = toDrop)
res.heatmap(vlim=[0,20],cname='-log2(p-value)')
figs['chipComparison'] = plt.gcf()

targetID = 'AT4G25470'
res = pyutil.mapper_2d(wFunc=lambda x,y: (targetID in (x.index & y.index)),
                       xs=it,ys=it
                      )
res = pd.DataFrame(res,columns=kit,index=kit)
res =scount.countMatrix(res)
toDrop = ['keyDFTrack']
res = res.drop(index=toDrop,columns = toDrop)
name = 'Contains-%s'%targetID
res.heatmap(cname=name)
figs['Contains-%s'%targetID] = plt.gcf()


cluFile= 'results/0408-cluster-CAMICE/0408-freezerCluster/results0408-prefiltering-camicetopped-20-nmsd-meannormpk/baseDist-vmfDistribution_seed-0/cluc.csv'
clu = pyext.readBaseFile(cluFile)
countDF = pyutil.get_cluCount(clu).sort_values('count')
cluIndex = clu.query('clu==@countDF.clu.iloc[-1]').index

res = pyutil.mapper_2d(wFunc=lambda x,y: 
                       pymisca.proba.index__getFisher(x.index & y.index, cluIndex,bkdIndex=bkdIndex)['p'],
                           xs= it,ys=it)
np.fill_diagonal(res,np.nan)
res = pd.DataFrame(res,columns=kit,index=kit)
res = res.apply(lambda x:-np.log2(x))
res = res.fillna(0.)
res =scount.countMatrix(res)
toDrop = ['keyDFTrack']
res = res.drop(index=toDrop,columns = toDrop)
res.heatmap(vlim=pyutil.span(res),cname='-log2(p-value)')
figs['intersecting-canonical-chx-responsive-genes'] = plt.gcf()

pyutil.render__images(figs)