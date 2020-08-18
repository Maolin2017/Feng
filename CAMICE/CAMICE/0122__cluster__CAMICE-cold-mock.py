#!/usr/bin/env python
# -*- coding: utf-8 -*-


NCORE = 6
execfile('/home/feng/meta/header_0903.py')
figs = pyutil.collections.OrderedDict()

url = 'http://172.26.114.34:81/static/figures/0122__prepareRNA__CAMICE/tracks.npy'
tracks = pyutil.readData(url).tolist()
tdf =tracks.cold_wt

import pymisca.model_collection.mixture_vmf as mod

if 1:
    data = tdf
    randomState = 0
    np.random.seed(randomState)
    nIter = 1600
    nStart = 1
#     betas = lambda i: (i + 1) * 0.00015 + 0.15
    callback = mod.callback__stopAndTurn(
        start=0.1,
        step=(10.0-0.1)/nIter)
#     callback = pyfop.composeF(callback__stopAndTurn(betas=betas),
# #                              callback__stopOnClu(interval=1)
#                              )
    mdl0 = mdl = mod.MixtureVMF(init_method = 'random',
                        NCORE=1,
#                          beta = betas(0),
                         weighted =  True,
                         normalizeSample=0,
                        kappa = None,
                        K = 20,)
    res = mdl.fit(
        data,verbose=2,
                  nStart=nStart,
                  callback = callback,
                  min_iters = nIter,
                  max_iters = nIter,
                  sample_weights=None,
                 )    
    np.save('mdl.npy',mdl0,)
    
mod.qc__vmf(mdl0)
figs['qcVMF'] = plt.gcf()
execfile('/home/feng/meta/footer__script2figure.py')

mdl = mdl0.callback.mdls[nIter//2][-1]
cacheFile = pyutil.cache__model4data(mdl=mdl,tdf=data,ofname='modelCache.npy')
