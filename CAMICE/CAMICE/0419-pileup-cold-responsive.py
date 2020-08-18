#!/usr/bin/env python2
import pymisca.header as pyhead
execfile(pyhead.base__file('headers/header__import.py'))
figs = pyutil.collections.OrderedDict()
FOLD_CHANGE_CUTOFF=6.


chipTks = pyext.readBaseFile('results/0224__chipTracks__CAMICE/tracks.npy').tolist()
chipTks.__dict__.pop('keyDFTrack',None)
lst = []
for k,v in chipTks.__dict__.items():
    v = v.iloc[:,0]
    v.name = k
    lst +=[v]
dfc =  pd.concat(lst,axis=1).fillna(0).astype(int)
dfc = dfc.sort_values(dfc.columns.tolist())
dfc.to_csv('chipTargetMatrix.csv')
#     print k,v.shape


cluFile= 'results/0408-cluster-CAMICE/0408-freezerCluster/0408-prefiltering-camicedataset_0411_coldonly_ratio_outcsv/baseDist-vmfDistribution_seed-0/clu.csv'
clu = pyext.readBaseFile(cluFile)
cluc = clu.query('clu==0 & score > 2.')
cluc.to_csv('cold-responsive-genes.csv')


ofname  = 'nearAUG-temp.tsv' 
mdfc = pyext.dir__indexify(pyext.base__file('results/0224__peak2gene__CAMICE/')).query('BASENAME.str.startswith("job_nearAUG")')
CMD = 'cat %s | head -1 > %s'  % (' '.join(mdfc['FULL_PATH']),ofname)
pyext.shellexec(CMD)
CMD = 'cat %s | grep -v start >> %s'  % (' '.join(mdfc['FULL_PATH']),ofname)
pyext.shellexec(CMD)

dfc = pyext.readBaseFile(ofname)
# dfc = pyext.readBaseFile('results/0224__peak2gene__CAMICE/job_nearAUG__peak_ICE1-cold.bed__cutoff_3000__feat_genes.gtf.cds.tsv',header=0)
dfcc = dfc.query('feat_acc in @cluc.index')
dfcc.to_csv('peak2gene.csv')
dfcc=  dfcc[sdio.bedHeader[:-1]].drop_duplicates()
dfcc = dfcc.query('FC> @FOLD_CHANGE_CUTOFF')
print (dfcc.shape)
pyext.to_tsv(dfcc,'pileup-regions.bed')


meta = mcurr = pyext.readBaseFile('results/0407-database-mapped/mcurr.csv')
# .reset_index()
# meta['FULL_PATH'] = meta['FULL_PATH.1']
mcurr  =mcurr.query('RUN_ID=="198C" & EXT=="bw"')[['BASENAME','DATAACC']]


mcurr = mcurr.sort_values('BASENAME')
it = pyext.nTuple(range(len(mcurr)),6)
# it = pyext.df__iterdict(mcurr)
for i,idx in enumerate(it):
# def job((i,idx)):
    def job():
        figs = pyext.collections.OrderedDict()


    #     with pyext.FrozenPath('Set%d'%i):
        bwCurr = mcurr.iloc[list(idx),]

    # for bwCurr in pyext.nTuple(list(it),6):
    #     print bwCurr
    #     bwCurr = pd.DataFrame(bwCurr)

        figs, bwTracks = sjob.figs__peakBW(bwFiles=bwCurr.index,
                                           outIndex=bwCurr['BASENAME'],
                          peakFile='../pileup-regions.bed');
    #     figs.update(figOut)
        pyutil.render__images(figs,exts=['png','svg'])
    pyext.func__inDIR(job, 'Set%d'%i)
# map()
#     plt.show()