#DOCUMENTS = ['document', 'response-to-editor']
#TEXS = [doc+".tex" for doc in DOCUMENTS]
#PDFS = [doc+".pdf" for doc in DOCUMENTS]
#FIGURES = ['fig1.pdf']

import os
#JOBDIR='BrachyPhoto'
os.environ.setdefault('BASE',os.getcwd())

rule check_deps:
    input: ['DEPS']
    output:
    shell:
        '''python2 -c "
import pymisca.ext as pyext;
pyext.execBaseFile('headers/header__import.py')
"'''
rule install_deps:
    input:
    output: temp('DEPS')
    shell:
        '''
pip2 install -r requirements.txt
sudo apt install -y bedtools
touch DEPS
'''
        
def parseList(buf):
    return buf.strip().replace(' ','').splitlines()
    
rule all:
    input:
        signals =[
            'results/0128__heatmap__Brachy/DONE',
            'results/0130__callDiffTarg__Brachy-ELF3/DONE',
            'results/0130__lineplot__pfr/DONE',],
    output:
    shell:
        "echo [DONE]"

rule decompress:
    input:
    output: 
        [directory('RNA-seq/'),]
    shell:
        "tar -xvzf  RNA-seq.tar.gz"
        

rule rnaCluster:
    input:
        scripts=['BrachyPhoto/0129__cluster__Brachy-RNA-all.py',
                'BrachyPhoto/0129__showCluster__Brachy-RNA-all.py',
                'BrachyPhoto/0128__heatmap__Brachy.py',],
        signals =
                ["results/0130__makeTracks-Brachy/DONE",],
    output:
        [
            "results/0129__showCluster__Brachy-RNA-all/DONE",
            "results/0129__cluster__Brachy-RNA-all/DONE",
            "results/0128__heatmap__Brachy/DONE",
        ]
        
    shell:
        '''python2 -c "
import pymisca.ext as pyext;
pyext.base__check()
# pyext.os.environ['BASE'] = '/home/feng/work'

suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0129__cluster__Brachy-RNA-all.py'),
#     env=env,
)
assert suc,res

suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0129__showCluster__Brachy-RNA-all.py'),
#     env=env,
)
assert suc,res

suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0128__heatmap__Brachy.py'),
#     env=env,
)
assert suc,res
"'''

rule chipTarget:
    output:
        "results/0130__callDiffTarg__Brachy-ELF3/DONE"
    input:
        scripts=
             ['BrachyPhoto/0130__makePeakWindows__Brachy-ELF3.py',
              'BrachyPhoto/0130__chipSummary__Brachy-ELF3.py',
              'BrachyPhoto/0130__callDiffTarg__Brachy-ELF3.py',
             ],
#         test = {output}
#         .strip().replace(' ','').splitlines()     
    shell:
        '''python2 -c "
import pymisca.ext as pyext;
pyext.base__check()

suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0130__makePeakWindows__Brachy-ELF3.py'),
#     env=env,
)
assert suc

suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0130__chipSummary__Brachy-ELF3.py')
)
assert suc

suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0130__callDiffTarg__Brachy-ELF3.py')
)
assert suc
"'''

rule misc:
    output:
         signals=
         ["results/0130__lineplot__pfr/DONE",],
#             ['results/%s/DONE'  % x.split('/')[-1].rsplit('.')[0] for x in input.scripts ],
    input:
         scripts=
             ['BrachyPhoto/0130__lineplot__pfr.py',
             ],
    shell:
        '''python2 -c "
import pymisca.ext as pyext;
pyext.base__check()
# pyext.os.environ['BASE'] = '/home/feng/work'

suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0130__lineplot__pfr.py'),
)
assert suc,res
"'''

rule heatmap:
    output: "results/0201__heatmap__Brachy/figure.html"
    input: 
        scripts=
            ['BrachyPhoto/0201__heatmap__Brachy.py',
            ],
        signals= 
            ['results/0130__makeTracks-Brachy/DONE',
            ],
    shell:
        '''python2 -c "
import pymisca.ext as pyext;
pyext.base__check()

suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0201__heatmap__Brachy.py'),
)
assert suc,res
"'''

rule loadRNA:
    input:
        ['RNA-seq/',]
    output:
        "results/0130__makeTracks-Brachy/DONE"
    shell:
        '''python2 -c "
import pymisca.ext as pyext;
pyext.base__check()

suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0131__dumpDataRNA__Brachy.py'),
)
assert suc,res

suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0130__makeTracks-Brachy.py'),
)
assert suc,res
"'''

rule dumpMeta:
    output:
    input:
    shell:
        '''python2 -c "
import pymisca.ext as pyext;
pyext.base__check()

suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0201__dumpMeta__Brachy.py'),
)
assert suc,res
"'''

        
rule archive:
    input:
    output:
    shell:
        '''python2 -c "
import pymisca.ext as pyext;
pyext.base__check()
suc,res = pyext.job__script(
    pyext.base__file('BrachyPhoto/0204__makeArchive__Brachy.py'),
)
assert suc,res
"'''        
        
        
        

        

rule date:
    input:
        "results/DONE_0128","results/DONE_0129"
HOST='localhost:8888'

rule temp1:
    input:
    output:
    shell:
        'echo {HOST}'
        
rule temp:
    input: ""
    output: "results/DONE_{date}"
    run:
        for i in {wildcards.date}:
            print(i)
            print (output[0])
            with open(output[0],'w') as f:
                f.write(i)
            #print(i,file=)