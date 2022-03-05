import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import math
os.chdir('/home/blackjack/rq')
csv=pd.read_csv('IsolationForest_Result_0227.csv')
csv=csv.loc[:,~csv.columns.str.contains("^Unnamed")]
#csv=addsomething(csv)
#csv.to_csv('IsolationForest_Result_0227.csv.csv')
up=1.5
down=0.7
a_r=math.pi
b_r=-a_r*1.5
a_l=math.pi/(2*0.3)
b_l=-a_l*0.7
def right(x):
    global br
    if (x>up):
        return math.sqrt(x-up)
    if (x==1):
        x+=0.03
#    br=max(br,abs(math.tan(a_r*x+b_r)))
    return (math.tan(a_r*x+b_r))


def left(x):
    global br
    if (x>down):
#        br=max(br,abs(1.5*math.tan(a_l*x+b_l)))
        if (x==1):
            x-=0.03
        return -1.5*math.tan(a_l*x+b_l)
    return 4/x-4/down
def calc(min_rate,max_rate,flag):
    if (min_rate>down and max_rate<up):
        lis[0]+=max(flag[1],flag[2])
#        print(min_rate,max_rate)
        return max(right(max_rate)*flag[2],left(min_rate)*flag[1])
    if (min_rate<down and max_rate>up):
        lis[1]+=flag[1]+flag[2]
        return right(max_rate)*flag[2]+left(min_rate)*flag[1]
    if (min_rate<down):
        lis[1]+=flag[1]
        return left(min_rate)*flag[1]
    lis[1]+=flag[2]
    return right(max_rate)*flag[2]
def remove(k):
    if (csv['restdays'][k]<60):
        return [1,0,0]
    if (k==0):
        return [0,1,1]
    if (last==-1 or csv['index'][k]!=csv['index'][last]):
        return [0,1,1]
    flag=1
    ret=[0,1,1]
    i=k-1
    while (i!=-1 and csv['index'][k]==csv['index'][i]):
        if (csv['min_rate'][i]>=down and csv['max_rate'][i]<=up):
            i-=1
            continue
        if (csv['min_rate'][i]<down and csv['min_rate'][k]<down and csv['min_end_date'][i]>=csv['date'][k]):
            ret[1]=0
        if (csv['max_rate'][i]>up and csv['max_rate'][k]>up and csv['max_end_date'][i]>=csv['date'][k]):
            ret[2]=0
        i-=1
    return ret
score=0
train=pd.read_csv('train_index_0228.csv')
lis=[0,0]
br=0
need_row_num=[]
for i in range(0,len(csv)):
    if (csv['index'][i] in list(train['index'])):
        tup=remove(i)
        if (tup[0]==1):
            continue
        if (tup[1]==tup[2]==0):
            continue
        if (csv['min_rate'][i]>0.7 and csv['max_rate'][i]<1.5):
            need_row_num.append(i)
        score+=calc(csv['min_rate'][i],csv['max_rate'][i],tup)
print(score)
print(lis)
need=csv.iloc[need_row_num]
print(len(need))
print(need)
need.to_csv('wrong.csv')
