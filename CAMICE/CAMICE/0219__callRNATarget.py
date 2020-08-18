#!/usr/bin/env python
# -*- coding: utf-8 -*-

execfile('/home/feng/meta/header_0903.py')
import pymisca.model_collection.mixture_vmf as mod;
figs = pyutil.collections.OrderedDict()

keyDF = pyutil.readData('/home/feng/meta/key_ath.csv')

url = 'http://172.26.114.34:81/static/figures/0122__prepareRNA__CAMICE/tracks.npy'
tks = rnaTracks = pyutil.readData(url).tolist()
tracks = rnaTracks.__dict__.values()
indDF = tracks[0]


tdf = pd.concat([
    tks.cold_wt,
    tks.chx_wt,
#     tks.cold_mut,
],axis=1)
tdf = scount.countMatrix(tdf).qc_Avg()
# tdf
marker = ['ATCBF1','ATCBF2']
ind = keyDF.query('BioName in @marker').index
markDF = tdf.reindex(ind)
# .values
L = pyutil.arr__l2norm(markDF.values,axis=1,keepdims=1)
markDF = markDF.values * 1./L
sig = markDF.mean(axis=0)

score = tdf.dot(sig).to_frame('score')

mm = pd.concat([tdf.summary,score],axis=1)
targClu = mm.eval('SD > 2. and score > 2.5').to_frame('clu')

pyvis.qc_2var(tdf.summary['SD'],score,nMax=-1,clu=targClu)

targClu.to_csv('clu.csv')

# markDF = pd.DataFrame(markDF)
# markDF.T.plot()