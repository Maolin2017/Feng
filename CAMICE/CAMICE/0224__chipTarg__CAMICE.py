#!/usr/bin/env python
# -*- coding: utf-8 -*-

# execfile("/home/feng/meta/header__script2figure.py")
import pymisca.header as pyhead
execfile(pyhead.base__file('headers/header__import.py'))
HOST = pyhead.base__check('HOST')

fname = 'metaio/simpleModel/Tag/json__chipTarg__CAMICE'
res = pyutil.readBaseFile(fname,ext='json', baseFile=HOST)
jobConfs = res = pyutil.read__buffer(res['fields']['text'],ext='json')


bwMeta = pyutil.readBaseFile('meta/meta_chip.tsv')
figs = pyutil.collections.OrderedDict()



worker = funcy.partial(sjob.job__chipTargPaired,
                       bwMeta = bwMeta)
for conf in jobConfs:
    for k in conf.keys():
        if k not in worker.func.func_code.co_varnames:
            print (k, conf.pop(k))
    res = worker(**conf)
    figs.update(res[0])
    # res = sjob.job__chipTargPaired(
#     bwMeta = bwMeta,
#     control='197CS4',
#     treatment='197CS5'
# )    
# execfile('/home/feng/meta/footer__script2figure.py')
pyutil.render__images(figs)