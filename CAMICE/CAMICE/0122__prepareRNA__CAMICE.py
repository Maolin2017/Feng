#!/usr/bin/env python
# -*- coding: utf-8 -*-

execfile('/home/feng/meta/header_0903.py')
figs=  pyutil.collections.OrderedDict()

fname = 'http://172.26.114.34:81/static/figures/0122__downloadRNA__CAMICE/files.json'
rnaFS = fs = pyutil.fileDict__load(fname)
rnaCurr = pyutil.readData(fs.rnaCurr,localise=True)
rnaDF = pyutil.readData(rnaFS.rnaDF,localise=True)

CUTOFF=0.3
rnaDF  = scount.countMatrix(rnaDF.dropna()).qc_Avg()
axs = pyvis.qc_2var(*rnaDF.summary[['per_MAX','per_SD']].values.T)
pyvis.abline(ax=axs[-1],x0=CUTOFF)
figs['qc1'] = plt.gcf()
rnaDF = rnaDF.reindex(rnaDF.summary.query("per_MAX>%s"%CUTOFF).index)
rnaDF = rnaDF.qc_Avg()
axs = pyvis.qc_2var(*rnaDF.summary[['per_MAX','per_SD']].values.T)
figs['qc2'] = plt.gcf()
rnaDF.to_csv('rnaDF.csv')

dfc = pyutil.readData('/home/feng/meta/meta__rna__CAMICE.tsv')
dfc = dfc.query('blacklisted!=1')
rnaCurr = dfc.merge(rnaMeta.drop(columns='bname'),left_index=True,right_index=True)
rnaCurr

keys = ['gtype','treatment','treatTime']
rnaCurr = rnaCurr.sort_values(keys)



query = 'gtype=="COL" and treatment=="COLD"'
dfc = rnaCurr.query(query)
print query
print ','.join(dfc.index)
print(dfc[['bname']].T.to_csv())

query = 'gtype=="COL" and treatment=="MOCK"'
dfc = rnaCurr.query(query)
print query
print ','.join(dfc.index)
print (dfc[['bname']].T.to_csv())

query = 'gtype=="COL" and treatment=="CHX"'
dfc = rnaCurr.query(query)
print query
print ','.join(dfc.index)
print (dfc[['bname']].T.to_csv())

query = 'gtype!="COL" and treatment=="MOCK" and treatTime.astype("float")==2'
dfc = rnaCurr.query(query)
print (dfc[['bname']].T.to_csv())

query = 'gtype!="COL" and treatment=="COLD" and treatTime.astype("float")==2'
dfc = rnaCurr.query(query)
print (dfc[['bname']].T.to_csv())

query = 'gtype!="COL" and treatment=="CHX" and treatTime.astype("float")==2'
dfc = rnaCurr.query(query)
print (dfc[['bname']].T.to_csv())


def trackMaker(buf,name,
#                vlim=[-3,3],
              vlim = None,
               
              ):
    contrast = pyutil.read__buffer(buf,ext='csv',header=None).T
#     contrast
    dfc = pyutil.df__makeContrast( rnaDF.dropna(), 
                                  contrast=contrast,
                                 )
    colMeta = pyutil.meta__makeContrast( rnaCurr.T.astype(str),contrast = contrast,
                                       sep='/').T
#     dfc = pyutil.df__makeContrast(dfc=rnaDF.dropna(),
#                             contrast=contrast,)
    if vlim is None:
#         vlim=[-3,3]
        vlim = pyutil.span(dfc)
        vlim = - np.mean(vlim) + vlim
        vlim=[-5,5]
    tdf = scount.countMatrix(dfc,colMeta=colMeta,
                            name=name,vlim=vlim)
#     tdf.relabel(colLabel='ZTime');
    return tdf

rnaTracks = pyutil.util_obj()

buf = '''
control,190RQS2,190RQS5,190RQS8,190RQS12,190RQS24,190RQS27
treatment,190RQS1,190RQS4,190RQS7,190RQS10,190RQS23,190RQS26
'''
name = 'COLD-MOCK_COL-COL'

rnaTracks['cold_wt'] =  trackMaker(buf,name).relabel('treatTime')


buf = '''
control,190RQS2,190RQS5,190RQS8,190RQS12,190RQS24,190RQS27
treatment,190RQS3,190RQS6,190RQS9,190RQS13,190RQS25,190RQS28
'''
name = 'CHX-MOCK_COL-COL'
rnaTracks['chx_wt'] =  trackMaker(buf,name).relabel('treatTime')

#### 191RQS6 is blacklisted and excluded along with 191RQS13
#### 191RQS11 replaced by 190RQS13 due to blacklisting
buf = '''
control,191RQS8,191RQS10,191RQS5,191RQS7,191RQS9,191RQS4
treatment,191RQS15,191RQS17,191RQS12,191RQS14,191RQS16,190RQS13
'''
name = 'CHX-MOCK_Mut-Mut'
rnaTracks['chx_mut'] =  trackMaker(buf,name).relabel('gtype')

buf ='''
control,191RQS8,191RQS10,191RQS5,191RQS7,191RQS9,191RQS4
treatment,191RQS1,191RQS3,191RQS30,191RQS32,191RQS2,191RQS29
'''
name = 'COLD-MOCK_Mut-Mut'
rnaTracks['cold_mut'] =  trackMaker(buf,name).relabel('gtype')

buf = '''
control,190RQS12,190RQS12,190RQS12,190RQS12,190RQS12,190RQS12,190RQS12,190RQS12,190RQS12,190RQS12
treatment,190RQS13,190RQS14,190RQS15,190RQS16,190RQS17,190RQS18,190RQS19,190RQS20,190RQS21,190RQS22
'''
name = 'CHEM-MOCK_COL-COL'
rnaTracks['chem_wt'] =  trackMaker(buf,name).relabel('treatment')


trackFile = 'tracks.npy'
np.save(trackFile, rnaTracks)

pyutil.fileDict__save(d=locals(),keys=['trackFile'],
                      fname='files.json')

execfile('/home/feng/meta/footer__script2figure.py')