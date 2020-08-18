#!/usr/bin/env python
# -*- coding: utf-8 -*-

# execfile("/home/feng/meta/header__script2figure.py")
import pymisca.header as pyhead
execfile(pyhead.base__file('headers/header__import.py'))
bwMeta = pyutil.readBaseFile('meta/meta_chip.tsv')
figs = pyutil.collections.OrderedDict()
# ylab  =

res = sjob.job__chipTargPaired(bwMeta = bwMeta,
                               control='197CS4',
                               treatment='197CS5')    
figs.update(res[0])
# execfile('/home/feng/meta/footer__script2figure.py')
pyutil.render__images(figs)