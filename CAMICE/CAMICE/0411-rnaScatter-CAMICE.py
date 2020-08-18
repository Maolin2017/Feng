#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymisca.header as pyhead
execfile(pyhead.base__file('headers/header__import.py'))
figs = pyutil.collections.OrderedDict()

keyDF = pyutil.readData('/home/feng/meta/key_ath.csv')

HOST = pyhead.base__check('HOST')

gconf = pyutil.readBaseFile('results/0219__prepareGCONF__Ath/gconf.npy').tolist()


cluFile = '/home/feng/work/results/0224__showCluster__CAMICE/clu.csv'
rnaClu = pyutil.readData(cluFile)

#### Load Tracks
chipTks = pyutil.readBaseFile('results/0224__chipTracks__CAMICE/tracks.npy').tolist()

# url = 'http://172.26.114.34:81/static/figures/0122__prepareRNA__CAMICE/tracks.npy'
url = 'results/0224__prepareRNA__CAMICE/tracks.npy'
tks = rnaTks = rnaTracks = pyutil.readBaseFile(url).tolist()
for v in vars(rnaTks).values():
    v.height = 4.
    


buf = '''
index,alias
190RQS7__190RQS8,1h-COLD/1h-MOCK
190RQS10__190RQS12,2h-COLD/2h-MOCK
190RQS9__190RQS8,1h-CHX/1h-MOCK
190RQS13__190RQS12,2h-CHX/2h-MOCK

190RQS10__190RQS9,2h-COLD/1h-CHX
190RQS13__190RQS7,2h-CHX/1h-COLD

# cold-mut
191RQS1__191RQS8,C24-2h-COLD/C24-2h-MOCK
191RQS3__191RQS10,CYHr1-2h-COLD/CYHr1-2h-MOCK
191RQS30__191RQS5,camta123-2h-COLD/camta123-2h-MOCK
191RQS32__191RQS7,ice1-1-2h-COLD/ice1-1-2h-MOCK
191RQS2__191RQS9,los1-1-2h-COLD/los1-1-2h-MOCK
191RQS29__191RQS4,Col-0-2h-COLD/Col-0-2h-MOCK

# chx-mut
191RQS15__191RQS8,C24-2h-CHX/C24-2h-MOCK
191RQS17__191RQS10,CYHr1-2h-CHX/CYHr1-2h-MOCK
191RQS12__191RQS5,camta123-2h-CHX/camta123-2h-MOCK
191RQS14__191RQS7,ice1-1-2h-CHX/ice1-1-2h-MOCK
191RQS16__191RQS9,los1-1-2h-CHX/los1-1-2h-MOCK
190RQS13__191RQS4,2h-CHX/Col-0-2h-MOCK
'''
# print buf

rowMeta = pyutil.read__buffer(buf,ext='csv')
print (rowMeta.to_csv(sep='\t'))


# print tks.chx_mut.colMeta[['alias']].to_csv()
xconfs = [
    ### wt: cold or chx at 1 or 2 hrs
    dict(ys='190RQS9__190RQS8', xs='190RQS7__190RQS8'),
    dict(ys='190RQS10__190RQS12', xs='190RQS13__190RQS12'),
    dict(ys='190RQS10__190RQS9',xs = '190RQS13__190RQS7'),
    
    ## cold mut
    dict(ys='191RQS3__191RQS10',xs='191RQS29__191RQS4'),
    dict(ys='191RQS30__191RQS5',xs='191RQS29__191RQS4'),
    dict(ys='191RQS32__191RQS7',xs='191RQS29__191RQS4'),
    dict(ys='191RQS2__191RQS9',xs='191RQS29__191RQS4'),
    
    ## chx-mut
    dict(ys='191RQS17__191RQS10',xs='190RQS13__191RQS4'),
    dict(ys='191RQS12__191RQS5',xs='190RQS13__191RQS4'),
    dict(ys='191RQS14__191RQS7',xs='190RQS13__191RQS4'),
    dict(ys='191RQS16__191RQS9',xs='190RQS13__191RQS4'),

]





def _parse(rnaDF,xs):
    treatment,control = xs.split('__')
    xs = pyutil.df__makeContrast(control=[control],treatment=[treatment],
                            dfc=rnaDF)
    return xs

def worker(xs,ys,rnaDF,clu=None,ax=None,xlim=None,ylim=None,labDF=None,silent=1):

    if isinstance(xs,basestring):
        xs = _parse(rnaDF,xs)
    if isinstance(ys,basestring):
        ys = _parse(rnaDF, ys)
    if ax is not None:
        axs = [None,ax,None,None]
    else:
        axs = None
    if silent:
        pass
    else:
        data = pd.concat([xs,ys,clu],axis=1)
        data.columns = ['xs','ys','clu']
        print data.head()
#         print '[%s]'%type(data.xs)
#         pyext.span(data.xs)
#         data= pd.Data(dict(xs=list(xs),ys=list(ys),clu=list(clu)),axis=1)
        axs = pyvis.qc_2var( data['xs'],data['ys'],axs=axs,clu=data['clu'],
                           refline=None)
        axs[1].set_xlim(xlim)
        axs[1].set_ylim(ylim)
        if labDF is not None:
            xlab,ylab = labDF.iloc[:,0].reindex([xs.columns[0],ys.columns[0]]).values
            axs[1].set_xlabel(xlab)
            axs[1].set_ylabel(ylab)
        title = 'color=%s'%getattr(clu,'name',None)
        
#         cmap = plt.get_cmap('Set1')
        colors = pyvis.color__defaultCycle()
        lines = []
        for i,(key,df) in enumerate( data.groupby('clu') ):
            k, c = pyext.arr__polyFit(df['xs'],df['ys'])
#             color = cmap(i)
            color = colors[i]
            pyvis.abline(k,c,color=color)
            eqn = 'y=%.3fx+%.3f'%(k,c)
#             eqn = pyvis.eqn_lm((k,c))
            title += '\n Key={key}, Eqn={eqn}' .format(**locals())
        
        
        axs[1].set_title(title)
        ax.legend()
        
    return dict(xs=xs,ys=ys)

_worker = funcy.partial(worker,
                       rnaDF = rnaTks.rnaDF,
                        labDF=rowMeta,
#                         xlim=[-5,5],ylim=[-5,5],
                       )
__worker = lambda kw:_worker(silent=1,**kw)
rowData = map( __worker,xconfs)

    

index = tks.rnaDF.index
for k,v in chipTks.__dict__.items():
    v = v.reindex(index).fillna(False)
    chipTks[k] = v

# it = rowData
import itertools
# colData = pyutil
colData=[

dict(clu=scount.countMatrix(
    rnaClu.eval("clu==2"),name='rnaClu-EQ-2')),
    dict(clu= chipTks['ICE1-cold'],),
    dict(clu = chipTks['ICE1-CHX']),
    dict(clu = chipTks['CAMTA-cold']),
    dict(clu= chipTks['CAMTA-CHX194']),
]

colData = [dict(clu=x['clu'].reindex(index).fillna(False)) 
           for x in colData]
np.save('rowData.npy',rowData)
np.save('colData.npy',colData)

it= itertools.product(rowData,colData)
it = list( dict(x.items() + y.items()) for x,y in it)

fig,axs=pyvis.get_subplotGrid(L=len(it),
                              ncols=len(colData),
                              baseColSep=6,
                              baseRowSep=6,
#                               baseColSep=0,baseRowSep=0
                             )
for i,row in enumerate(it):
    row['ax'] = axs[i]
    
_worker = funcy.partial(worker,
                       rnaDF = rnaTks.rnaDF,
                        labDF=rowMeta,
                        xlim=[-5,5],ylim=[-5,5],
                       )
__worker = lambda kw:_worker(silent=0,**kw)
_ = map( __worker,it)

figs['correlationMatrix'] = fig

pyutil.render__images(figs,
                      exts=['png','svg']
                     )
ax = plt.gca()