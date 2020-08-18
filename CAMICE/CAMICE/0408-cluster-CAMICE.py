#!/usr/bin/env python2
import pymisca.header as pyheader
pyheader.base__check()
pyheader.execBaseFile('headers/header__import.py')
figs = pyext.collections.OrderedDict()
# %%time
# __file__
def worker(seed,stepSize=None):
    print seed
#     re = 1.00001
#     re = 0.00001
    re = 0.
    query = "per_SD > 0.95"
#     baseDist = 'alignedGaussianDistribution'
    baseDist = 'vmfDistribution'
#     data = 'results/0407-prefiltering-CAMICE/topped-20-nmsd-meannorm.pk'
#     data = 
#     data = 'results/0408-prefiltering-CAMICE/topped-20-nmsd-meannorm.pk'
#     data = 'results/0408-prefiltering-CAMICE/DATASET_0409/topped-20-nmsd-meannorm.pk'

#     data = 'results/0408-prefiltering-CAMICE/DATASET_0411_COLDONLY/topped-20-nmsd-meannorm.pk'
    data = 'results/0408-prefiltering-CAMICE/DATASET_0411_COLDONLY_RATIO_/out.csv'
#     data = 'headers/mnist.csv'

#     script = 'src/0408-freezerCluster.py'
    
    suc, res = pyext.job__scriptCMD(
        'repos/pymisca/bin/0408-freezerCluster.py \
--data {data} \
--quick 60 \
--cluMax 30 \
--start 0.01 \
--end 30. \
--XCUT 75 \
--debug 1 \
--query "{query}" \
--seed {seed} \
--baseDist {baseDist} \
\
--width_ratios 3 10 0 \
'.format(**locals()),
     prefix='results/%s'%pyext.getBname(__file__),
    baseFile=1,
    )

    assert suc,res
NJOB = 3
pyext.mp_map(worker,range(NJOB),NCORE=NJOB)