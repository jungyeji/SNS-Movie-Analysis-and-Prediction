import pandas as pd
import sys

readfilename=sys.argv[1]
encoding=sys.argv[2]

if not readfilename:
    print('python py_filename readfilename encoding')

data=pd.read_csv(readfilename, encoding=encoding)
size=len(data['MOVIENAME'])
pos=data['POS']
neg=data['NEG']

prop_list=[]
res_list=[]

for i in range(size):
    if pos[i]+neg[i]==0:
        prop_list.append('')
        res_list.append('')
    else:
        prop=pos[i]/(pos[i]+neg[i])
        prop_list.append(prop)
        if prop>=0.5:
            res_list.append('POS')
        else:
            res_list.append('NEG')

data['POS_NEG_RES']=res_list
data['POS_NEG_RATIO']=prop_list

data.to_csv(readfilename.split('.')[0]+'_judged.csv')
