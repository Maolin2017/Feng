#!/usr/bin/env python
# -*- coding: utf-8 -*-
NCORE=6
import pymisca.ext as pyext
execfile(pyext.base__file('headers/header__import.py'))
figs = pyutil.collections.OrderedDict()


gconf = pyutil.util_obj(**pyutil.envSource(
    pyext.base__file('ref/config/config_Ath_TAIR10.sh'),silent=1)
                       )
keyDF = pyutil.readBaseFile('headers/key_ath.csv')
if hasattr(keyDF,'gconf'):
    anno = pyutil.readBaseFile(gconf.ANNOINFO)
    dfc = pyutil.readBaseFile(gconf.ANNOINFO,comment=None)
    dfc = dfc.sort_values('transcriptName')
    dfc = dfc.query('~locusName.duplicated()').set_index('locusName')
    dfc = dfc['Best-hit-arabi-name,arabi-symbol,arabi-defline'.split(',')]
    gconf.defline = defline = dfc
    # Best-hit-arabi-name      arabi-symbol    arabi-defline

    # defline = pyutil.readData(gconf.DEFLINE,header = None)
    # defline.index = defline.index.str.split('.',1).str.get(0)
    # defline = defline[[2]].rename(columns = {2:'defline'})
    # defline = defline.query('~index.duplicated()')
    # gconf.defline = defline

    gene2name =dfc= pyutil.readBaseFile(gconf.GENE2NAME,header = None, names = list(range(3)))

    ### patch 
    rid = ~dfc[2].isnull()
    dfcc = dfc.loc[rid]
    cid = dfcc.applymap(len).values.argmin(axis=1)
    rid = np.where(rid)[0][cid]
    dfc.iloc[rid,0] = dfc.iloc[rid,1]

    dfc.index = dfc.index.str.split('.',1).str.get(0)

    if 0:
        dfc =  dfc[[1]].rename(columns={1:'synonym'})
        dfc.loc['Bradi5g13980'] = 'BdCDKG'
        dfc = dfc.query('~synonym.duplicated()')
        keyDFC = sutil.tidyBd(keyDF)
        dfc=dfc.merge(right=keyDFC ,how='outer',left_index=True,right_index=True)[['synonym']]
        dfc = dfc.fillna(keyDFC.rename(columns={'BioName':'synonym'}))

        gconf.gene2name = gene2name = dfc



    gconf.geneMeta = geneMeta = pd.concat([gene2name,defline],axis=1,sort=True)
    geneMeta.to_csv('geneMeta.csv')
np.save('gconf.npy',gconf)

# %timeit defline.index.str.extract('([^\.]+)')
# %timeit defline.index.str.split('.',1).str.get(0)