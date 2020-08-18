#!/usr/bin/env python2
import pymisca.header as pyheader
pyheader.base__check()
pyheader.execBaseFile('headers/header__import.py')
figs = pyext.collections.OrderedDict()
# meta= pyext.dir__indexify('/home/feng/writable/teamkj/__backup/')

keys = ['GTYPE','TREATMENT','TEMP','TREATTIME','DATAACC']

colMeta = pyext.readBaseFile('meta/meta__rna__CAMICE.tsv',guess_index=0)
colMeta.columns = colMeta.columns.str.upper()
colMeta = colMeta.sort_values(keys)
colMeta = colMeta.set_index('DATAACC',drop=0)
colMeta['HEADER'] = pyext.df__format(colMeta,'-'.join('{%s}'%x for x in keys))

def checkShow(dfc):
    dfc = dfc[['RUN_ID','SAMPLE_ID','FILEACC','BASENAME']].reset_index(drop=1)
    print (dfc)
#     pyext.ipd.display(dfc)

mcurr = pyext.readBaseFile('results/0407-database-mapped/mcurr.csv',guess_index=0)
dfc = mcurr.copy()
dfc = dfc.query('RUN_ID=="200R"')
dfc  = dfc.query('BASENAME=="read_counts.txt"')
checkShow(dfc)
dfc.to_csv('mcurr.csv')



lst = map( funcy.partial(pyext.readBaseFile,header=None),
          dfc['FULL_PATH'])

tab = pd.concat(lst,axis=1)
tab.columns = dfc['DATAACC']
tab = tab.query('~index.str.startswith("__")')
rnaTable = tab.copy()
rnaTable.to_csv('rnaTable.csv')
    

# reload(synotil.qcplots)
# reload(sutil)
# rnaTable = pyext.readBaseFile('rnaTable')
tab = rnaTable.copy()

def qc():
    return sutil.qc_Sort(tab,nMax=-1,vlim=[0,12]);

blacklist = pyext.readBaseFile('headers/blacklist.csv',header=None).index
tab = tab.drop(columns=blacklist,errors='ignore')

CUTOFF = 20
tab  = sdio.df__topupANDdrop(tab,CUTOFF=CUTOFF,threshold=3)
tab = tab.apply(np.log2)
# tab = tab.query('columns !="200RS4"')
# tab = tab.apply(pyext.log2p1)

# sutil.qc_Sort(tab,nMax=-1,vlim=[0,12]);
tab = scount.countMatrix(tab).qc_Avg();
tab = tab.reindex(columns = pd.Index(colMeta['DATAACC']) & tab.columns)
tab.set__colMeta(colMeta)
tab = tab.relabel(colLabel='HEADER')
tab = tab.reindex(tab.summary.query('SD!=0').index)

const,vdf = sutil.qc_libsize(tab,silent=0);
figs['qc__libSize1'] = plt.gcf()

def saveData(ALIAS):
    vdf.to_csv('%s.csv'%ALIAS)
    vdf.to_pickle('%s.pk'%ALIAS)
    
ALIAS = 'topped-{CUTOFF}-nmsd'.format(**locals())
saveData(ALIAS)

vdf = sutil.meanNorm(vdf.copy())
ALIAS += '-meannorm'
saveData(ALIAS)

vdf1 = sutil.meanNorm(vdf.copy()).reindex(vdf.summary.sort_values('SD').index)
vdf1.heatmap(figsize=[12,8],vlim=[-2,2])
figs['qc__libSize2'] = plt.gcf()

tab = vdf
res = qc()
figs.update(res[-1])
# figs['qcSort'] = plt.gcf()
pyutil.render__images(figs, )