#!/usr/bin/env python
# -*- coding: utf-8 -*-

# execfile("/home/feng/meta/header__script2figure.py")
NCORE=1
import pymisca.header as pyheader
pyheader.base__check()
execfile(pyheader.base__file('headers/header__import.py'))
HOST = pyheader.base__check('HOST')



# fname = 'metaio/simpleModel/Tag/0322-chipTarg-198C.json'
# res = pyutil.readBaseFile(fname,ext='json', baseFile=HOST)
# jobConfs = res = pyutil.read__buffer(res['fields']['text'],ext='json')

# jobConfs = pyutil.readBaseFile('CAMICE/0322-chipTarg-198C.json')
jobConfs = pyutil.readBaseFile('CAMICE/0411-chipTarg-CBF2-198C.json')

bwMeta = pyutil.readBaseFile('meta/meta_chip.tsv')
figs = pyutil.collections.OrderedDict()



worker = funcy.partial(sjob.job__chipTargPaired,
                       bwMeta = bwMeta)
# assert 0
#     for conf in jobConfs:
def _worker(conf):
    try:
        for k in conf.keys():
            if k not in worker.func.func_code.co_varnames:
                print (k, conf.pop(k))
        res = worker(**conf)
    except Exception as e:
        raise Exception(str(e) +'\n'+ str(conf))
    return res[0]

# res = _worker(
#     pyext.collections.OrderedDict([(u'CUTOFF_CHIPDIFF', 1.0), (u'CUTOFF_FC', 3.0), (u'name', u'198C-ICE1-CHX-R2'), (u'control', u'198CS1'), (u'treatment', u'198CS3')])
#              )
#     figs.update(res[0])
res = pyutil.mp_map(_worker,jobConfs, NCORE=NCORE)
[figs.update(x) for x in res]

# execfile('/home/feng/meta/footer__script2figure.py')
pyutil.render__images(figs)