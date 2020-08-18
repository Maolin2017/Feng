#!/usr/bin/env python
# -*- coding: utf-8 -*-

execfile('/home/feng/meta/header_0903.py')
figs=  pyutil.collections.OrderedDict()



# fname = 'http://172.26.114.34:81/static/figures/0104__prepareRNA__CAMICE/files.json'
# rnaFS = fs = pyutil.fileDict__load(fname)
# rnaCurr = pyutil.readData(fs.rnaCurrFile,localise=True)
# rnaDF = pyutil.readData(rnaFS.rnaDFFile,localise=True)
VALUE_COL = 'read_count'
# VALUE_COL = 'CPM'

# rnaCurr = pyutil.mergeByIndex(meta,rnaMeta.drop(columns='bname'),how='left')


dfc = pyutil.readData('/home/feng/meta/meta__rna__CAMICE.tsv')
dfc = dfc.query('blacklisted!=1')
rnaCurr = dfc.merge(rnaMeta.drop(columns=['bname','blacklisted']),
                    left_index=True,right_index=True)
rnaCurr


dfc= pyutil.readData_multiple(rnaCurr.query("pipeline=='star-quantseq'").fname)
dfcc = dfc.pivot_table(index='gene_id',columns='fname',
                       values=VALUE_COL)
dfcc.columns = dfcc.columns.map(pyutil.df2mapper(rnaCurr.reset_index(),'fname','DataAcc').get)
dfcc = dfcc.sort_index(axis=1)

dfcc.sum(axis=0).plot(xticks=range(len(dfcc.columns)),rot='vertical')
figs['qc0'] = plt.gcf()
rnaDF = dfcc.copy().apply(pyutil.log2p1)


CUTOFF=0.45
rnaDF  = scount.countMatrix(rnaDF.dropna()).qc_Avg()
axs = pyvis.qc_2var(*rnaDF.summary[['per_MAX','per_SD']].values.T)
pyvis.abline(ax=axs[-1],x0=CUTOFF)
figs['qc1'] = plt.gcf()
rnaDF = rnaDF.reindex(rnaDF.summary.query("per_MAX>%s"%CUTOFF).index)
rnaDF = rnaDF.qc_Avg()
axs = pyvis.qc_2var(*rnaDF.summary[['per_MAX','per_SD']].values.T)
figs['qc2'] = plt.gcf()
rnaDF.to_pickle('rnaDF.pk')
rnaCurr.to_csv('rnaCurr.csv')


pyutil.fileDict__save(d=dict(rnaDF='rnaDF.pk',
                            rnaCurr='rnaCurr.csv'),
                      fname='files.json')

execfile('/home/feng/meta/footer__script2figure.py')
