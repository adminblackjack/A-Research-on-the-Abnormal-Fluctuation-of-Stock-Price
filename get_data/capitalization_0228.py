import pandas as pd
import numpy as np
import rqdatac as rq
import os
import math
from jqdatasdk import finance
from jqdatasdk import *
from jqdatasdk.technical_analysis import *
path=os.getcwd()
os.chdir(path+'/2016-2019-data')
path=os.getcwd()
drop=pd.read_csv('drop.csv')
lis=os.listdir()
index=[]
total_shares=[]
close=[]
capitalization=[]
for i in range(0,len(lis)):
    if (lis[i][0]!='0' and lis[i][0]!='3' and lis[i][0]!='6'):
        continue
    if (lis[i] in drop['index']):
        continue

#    temp=rq.current_performance(lis[i],info_date='2019-12-31',fields='total_shares')
    os.chdir(path+'/'+lis[i])
    templist=os.listdir()
    if ((lis[i]+'_indicator_0204.csv') not in templist):
        continue
    print(i,lis[i])
    q=query(valuation.capitalization).filter(valuation.code==lis[i])
    temp=get_fundamentals(q,date='2019-12-30')
    total_shares.append((temp['capitalization'][len(temp)-1]*10000))
    csv=pd.read_csv(lis[i]+'_indicator_0204.csv')
    close.append(csv['close'][len(csv)-1])
    capitalization.append(close[-1]*total_shares[-1])
    index.append(lis[i])
save=pd.DataFrame(columns=('index','total_shares','capitalization'))
save['index']=index
save['total_shares']=total_shares
save['capitalization']=capitalization
print(path)
os.chdir('/home/blackjack/rq/2016-2019-data')
save.to_csv('capitalization.csv')
