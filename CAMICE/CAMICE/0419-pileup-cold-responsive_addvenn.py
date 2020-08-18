#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymisca.header as pyheader
pyheader.base__check()
execfile(pyheader.base__file('headers/header__import.py'))
figs = pyutil.collections.OrderedDict()

chipTks = pyutil.readBaseFile('results/0224__chipTracks__CAMICE/tracks.npy').tolist()
url = 'results/0224__prepareRNA__CAMICE/tracks.npy'
tks = rnaTks = rnaTracks = pyutil.readBaseFile(url).tolist()
bkdIndex = rnaTks.rnaDF.index
# chipTks['198C-CAMTA1-camta123-CHX-R2']
def plotter(xlab,ylab,ax=None):
#     ax = plt.gca()
#     if ax is None
#         ax = plt.gca()
#     xlab = 'CAMTA-CHX194'
#     ylab =  'ICE1-CHX'
    left = chipTks[xlab] 
    right = chipTks[ylab]
    indDF,ax = pyvis.qc_index(left.index,right.index,silent=0,
                              ax=ax,
                              xlab=xlab,ylab=ylab);
    ALIAS = '%s_%s'%(xlab,ylab)
    figs[ALIAS] = ax.figure
    indDF.to_csv(ALIAS+'.csv')
    return indDF,ax

def job():
    xlab = '198C-ICE1-cold-R2'
    ylab = '198C-CAMTA2-camta123-cold-R2'
    resDF,_ = plotter(xlab,ylab);

    xlab = '198C-ICE1-cold-R2'
    ylab = 'CAMTA-cold'
    resDF = pyvis.qc_index(chipTks[xlab].index, chipTks[ylab].index,xlab=xlab,ylab=ylab,
                  silent = 0);
    resDF,_ = plotter(xlab,ylab);

    xlab = '198C-ICE1-cold-R2'
    ylab = 'ICE1-cold'
    resDF,_ = plotter(xlab,ylab);
    pyutil.render__images(figs,exts=['png','svg'])
    

pyext.func__inDIR(job,pyext.base__file('results/0419-pileup-cold-responsive/venn_diagram',
                                      force=1,asDIR=1),)

# kit,it = zip(*chipTks.__dict__.items())