#!/usr/bin/env python
import pymisca.header as pyheader
pyheader.execBaseFile('headers/header__import.py')
figs = pyext.collections.OrderedDict()

np.random.seed(0)


if 1:
    rnaDF = pyext.readBaseFile('results/0122__downloadRNA__CAMICE/rnaDF.pk')
#     rnaDF = rnaDF.apply(lambda x:2**(x) - 1)
    rnaCurr = pyext.readBaseFile('results/0122__downloadRNA__CAMICE/rnaCurr.csv')
    def dropByNonZeroCount(dfc,CUTOFF = 0., threshold = 2, inplace=False):
        
        SUM = (dfc> CUTOFF).sum(axis=1)

        toDrop = SUM.to_frame('SUM').query('SUM<%d' % threshold).index
        dfc = dfc.drop(index=toDrop,inplace=inplace)
        return dfc        
    
    def getData():
        sutil.qc_Sort(rnaDF,nMax=-1)
        # tdf = rnaDF.query()
        query = 'gtype=="COL" and treatment=="COLD" | gtype=="COL" and treatment=="MOCK" |gtype=="COL" and treatment=="CHX" '
        dfc = rnaCurr.query(query)
        tdf = rnaDF.reindex(columns=dfc.index)
        dfc = dropByNonZeroCount(dfc, CUTOFF = np.log2(30 + 1))
        
        tdf.head()
        tdf = sutil.stdNorm(tdf.copy())
        return tdf


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--quick', default = 1, type=int)
parser.add_argument('--XCUT', default = 40, type=int)
parser.add_argument('--YCUT', default = 1.5, type=float)
parser.add_argument('--start', default = 0.25, type=float)
parser.add_argument('--end', default = 4.0, type=float)
def main(
    XCUT = None,
    # XCUT = 50
    YCUT = None,
    figsize=[ 22, 8 ],
    quick = None,
    start = None,
    end = None, 
    
):
    print (type(quick))
    dfc=  getData()
#     start,end = [0.25, 4.]
    
    # keys =  [u'Age',  u'ZTime', u'gtype', u'light',]

    # XCUT = 11
    # YCUT = 1.5
    # figsize=[22,8]
    keys =  [  u'light',
             'treatment',
             u'treatTime',
             u'gtype',]
    keys = filter( lambda x:x in rnaCurr, keys)

    #### start clustering
    if quick == 1:
        mdl0 = pyjob.vmfMixture__anneal(dfc, start, end,K=10,
                                        nIter=50)

    elif quick ==0 :
        mdl0 = pyjob.vmfMixture__anneal(dfc, start, end,K=30,
                                        nIter=200)
    if quick != -1:
        np.save('mdl0.npy',mdl0)
    else:
        mdl0 = np.load('mdl0.npy').tolist()

    pycbk.qc__vmf__speed(mdl0,XCUT=XCUT,YCUT=YCUT)
    figs['qcVMF'] = plt.gcf()


    ##### Post visualisation

    # mdl0 = np.load('mdl0.npy').tolist()


    mdl = mdl0.callback.mdls[XCUT][-1]
    clu  = mdl.predictClu(mdl0.data,entropy_cutoff = YCUT,index=mdl0.data.index)
    # score = mdl.score(mdl0.data)
    score = pyutil.logsumexp( 
        mdl._log_pdf(mdl0.data),axis=1)
    clu['score'] = score
    print pyutil.get_cluCount(clu).T
    clu.to_csv('clu.csv')
    
    vdf = dfc.copy()
    vdf = vdf.reindex(columns = rnaCurr.index & vdf.columns)
    vdf=  scount.countMatrix(vdf,colMeta = rnaCurr)
    # vdf =sutil.sumNorm(scount.countMatrix(rnaTable.astype(float),
    #                                      colMeta =rnaCurr))
    # .apply(np.sqrt)
    vdf.relabel(colLabel=keys)

    # clu.clu.replace({0:3,1:3,2:3},inplace=True)

    if 1:
        clu.hist('score',bins=30)
        figs['hist-score'] = plt.gcf()

    if 1:
        pp = spanel.panelPlot([spanel.fixCluster(clu['clu']), 
                               vdf,
                              ],figsize=figsize,
                              width_ratios=[2,10,0],

                               show_axa=1
                             )
        # pp.render(order = clu )
        fig = pp.render(order = clu,
                  index = clu.query('clu>=-1').index
                 );
        figs['heatmap-all'] = fig

    if 1:
        pp = spanel.panelPlot([spanel.fixCluster(clu['clu']), 
                               vdf,
                              ],figsize=figsize,
                              width_ratios=[2,10,0],

                               show_axa=1
                             )
        index = clu.query('clu>=-1 & score > 10.').index
        if len(index)==0:
            index = None
        pp.render(order = clu,
                  index = index
                 );

        figs['heatmap-filter'] = fig
    pyutil.render__images(figs)
if __name__ == '__main__':
    args = parser.parse_args()
    main(**vars(args))
    # ;pp.render(order = clu,
    #           index = clu.query('clu>=0').index);