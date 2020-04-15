from konlpy.tag import Mecab
import csv
import numpy as numpy
import re
import pandas as pd
from pandas import Series, DataFrame
from itertools import chain
import time
import sys


start_time=time.time()

#파일 불러오기
readfilename=sys.argv[1]
encoding=sys.argv[2]

data = pd.read_csv(readfilename, encoding=encoding)
reviews=data['REVIEW_PRE']
print('불러오기 완료')
#print(reviews)

mecab=Mecab()


#revie_pre 형태소 분석

mor_list=[]
for i in range(len(reviews)) :
	if(i%1000==0):
		print('i: ', i)
	li=['/'.join(t) for t in mecab.pos(reviews[i])]
	mor_list.append(li)
	
	
#print(mor_list)

#data_text = reviews.map(review_text)
print('형태소 분석 완료')

#print(data_text)

posdic={}
polf=open('polarity_plus.csv', 'r',encoding='cp949')
reader=csv.DictReader(polf)
for row in reader:
	posdic[row['ngram']]=row['max.value']
	
polf.close()

#print(posdic)
new_mor={}

pos_list=[]
neg_list=[]
neut_list=[]
logfile=open('log.txt', 'w', encoding='utf-8')
for text in mor_list:
	positive=0
	negative=0
	neutral=0
	l=len(text)
	for w in range(l):
		for i in range(3):
			key=''
			
			if ((i==1) and (w+1<l)):
				key=text[w]+';'+text[w+1]
			elif(i==2 and w+2<l):
				key=text[w]+';'+text[w+1]+';'+text[w+2]
			elif(i==0):
				key=text[w]
			
				
			try:
				if posdic[key]=='POS':
					positive=positive+1
					#print(key,': pos')
					#logfile.write('%s, : pos\n'%key)
				elif posdic[key]=='NEG':
					negative=negative+1
					#print(key, ': neg')
					#logfile.write('%s, : neg\n'%key)
				elif posdic[key]=='NEUT':
					neutral=neutral+1
					#print(key, ': neut')
					#logfile.write('%s, : neut\n'%key)
			except:
				try:
					new_mor[key]=new_mor[key]+1
				except:
					new_mor[key]=1
				#print('긍부정 사전에 없는 단어: ' , key)
				
	
	pos_list.append(positive)
	neg_list.append(negative)
	neut_list.append(neutral)
	
	#print(positive, negative, neutral)

data['POS']=pos_list
data['NEG']=neg_list
data['NEUT']=neut_list


fname=readfilename.split('.')[0]+'_posneg_result_%d.csv'%len(mor_list)
data.to_csv(fname, encoding='utf-8', mode='w')


'''
new_mor_file=open('new_mor.csv', 'w', newline='')
wr=csv.writer(new_mor_file)
for k in new_mor:
	if new_mor[k]>=10:
		wr.writerow([k, new_mor[k]])
new_mor_file.close()
'''

	
	

end_time=time.time()
print(end_time-start_time)

