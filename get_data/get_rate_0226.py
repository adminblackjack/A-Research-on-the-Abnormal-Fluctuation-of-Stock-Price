import os
import pandas as pd
import numpy as np
path=os.getcwd()
print(path)
os.chdir(path+'/2016-2019-data')
path=os.getcwd()
print(path)
lis=os.listdir()
drop=pd.read_csv('drop.csv')
drop=drop.loc[:,~drop.columns.str.contains("^Unnamed")]
A=[]
index=[]
class section:
    def __init__(self,index='0',start_date='0',end_date='0',days=0,rate=1,start_price=0,end_price=0):
        self.index=index
        self.start_date=start_date
        self.end_date=end_date
        self.days=days
        self.rate=rate
        self.start_price=start_price
        self.end_price=end_price
for i in range(0,len(lis)):
    start_date=[]
    days=[]
    start_price=[]
    rate=[]
    print(len(A))
    if (lis[i][0]!='6' and lis[i][0]!='3' and lis[i][0]!='0'):
        continue
    if (lis[i] in drop['index']):
        continue
#    lis[i]='000001.XSHE'
    os.chdir(path+'/'+lis[i])
    templis=os.listdir()
    if ((lis[i]+'_indicator_0204.csv') not in templis):
        continue
    suspend=pd.read_csv(lis[i]+"_suspend.csv")
    csv=pd.read_csv(lis[i]+'_indicator_0204.csv')
    high=pd.read_csv(lis[i]+'_new.csv')
    lencsv=len(csv['date'])
    print(lis[i])
#    if (lencsv<=250):
#        continue
    for j in range(0,lencsv):
#        if (j<120):
#            continue
        min60=10000
        min60d='0'
        d=0
        sd='0'
        ed='0'
        sp=0
        ep=0
        for k in range(j-60,j+1):
            if (k<0):
                continue
            if (min60>=csv['low'][k] or min60d=='0'):
                min60=csv['low'][k]
                min60d=csv['date'][k]
                d=j-k
                sd=csv['date'][k]
        start_date.append(min60d)
        days.append(d)
        start_price.append(min60)
        rate.append(high['high'][k]/min60)
    csv['start_date']=start_date
    csv['days']=days
    csv['rate']=rate
    csv['start_price']=start_price
    A.append(lis[i])
    csv.to_csv(lis[i]+'_rate_0226.csv')
