import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import math
def addsomething(df):
    date=[]
    restdays=[]
    path=os.getcwd()
    os.chdir(path+'/2016-2019-data')
    path=os.getcwd()
    for i in range(0,len(df)):
        os.chdir(path+'/'+df['index'][i])
        tempdf=pd.read_csv(df['index'][i]+'_rate_0226.csv')
        date.append(tempdf['date'][df['row_num'][i]])
        restdays.append(len(tempdf)-df['row_num'][i]-1)
        print(i)
    df['date']=date
    df['restdays']=restdays
    return df
os.chdir('/home/blackjack/rq')
csv=pd.read_csv('IsolationForest_Result_0227.csv')
csv=csv.loc[:,~csv.columns.str.contains("^Unnamed")]
csv=addsomething(csv)
#csv.to_csv('IsolationForest_Result_0227.csv.csv')
plt.figure(figsize=(40,20))
#plt.hist(csv['max_rate'],bins=60,range=(1,4))
lis=[0,0]
def right(x):
    if (x>1.4):
        return 5*(x-1.4)
    if (x==0.7):
        x+=0.1
    return 5*math.log(x-0.7)

def left(x):
    if (x>0.7):
        if (x==1):
            x+=0.1
        return math.log(abs(x-1))
    return 4/x

def calc(min_rate,max_rate):
    if (min_rate>0.7 and max_rate<1.4):
        lis[0]+=1
#        print(min_rate,max_rate)
        return right(max_rate)+left(min_rate)
    if (min_rate<0.7 and max_rate>1.4):
        lis[1]+=2
        return right(max_rate)+left(min_rate)
    if (min_rate<0.7):
        lis[1]+=1
        return left(min_rate)
    lis[1]+=1
    return right(max_rate)
print(csv)
os.chdir('/home/blackjack/rq')
csv.to_csv('IsolationForest_Result_0227.csv')
score=0
train=pd.read_csv('train_index_0228.csv')
cnt=0
for i in range(0,len(csv)):
    if (csv['index'][i] in list(train['index'])):
        if (csv['restdays'][i]<60):
            continue
        score+=calc(csv['min_rate'][i],csv['max_rate'][i])
        cnt+=1
print(score,cnt,score/cnt)
print(lis)
