import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import math
def right(x):
    global br
    if (x>up):
        return math.sqrt(x-up)
    if (x==1):
        x+=0.03
#    br=max(br,abs(math.tan(a_r*x+b_r)))
    return min(-5*(x-up),math.tan(a_r*x+b_r))


def left(x):
    global br
    if (x>down):
#        br=max(br,abs(1.5*math.tan(a_l*x+b_l)))
        if (x==1):
            x-=0.03
        return min(-6*(x-down),-1.5*math.tan(a_l*x+b_l))
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
    flag=1
    ret=[0,1,1]
    i=k-1
    while (i!=-1 and csv['index'][k]==csv['index'][i]):
        if ((csv['min_rate'][i]>=down and csv['max_rate'][i]<=up) or used[i]==0):
            i-=1
            continue
        if (csv['min_rate'][i]<down and csv['min_rate'][k]<down and csv['min_end_date'][i]>=csv['date'][k]):
            ret[1]=0
        if (csv['max_rate'][i]>up and csv['max_rate'][k]>up and csv['max_end_date'][i]>=csv['date'][k]):
            ret[2]=0
        i-=1
    return ret
def get_score(csv_name):
    global up
    up=1.5
    global down
    down=0.7
    global a_r
    a_r=math.pi
    global b_r
    b_r=-a_r*1.5
    global a_l
    a_l=math.pi/(2*0.3)
    global b_l
    b_l=-a_l*0.7
    os.chdir('/home/blackjack/rq')
    global csv
    csv=pd.read_csv(csv_name+'.csv')
    csv=csv.loc[:,~csv.columns.str.contains("^Unnamed")]
    #csv=addsomething(csv)
    #csv.to_csv('IsolationForest_Result_0227.csv.csv')
    score=0
    train=pd.read_csv('train_index_0306.csv')
    global lis
    lis=[0,0]
    br=0
    global wrong_row_num
    wrong_row_num=[]
    global used
    used=[]
    for i in range(0,len(csv)):
        if (csv['index'][i] in list(train['index'])):
            tup=remove(i)
            if (tup[0]==1):
                used.append(0)
                continue
            if (tup[1]==tup[2]==0):
                used.append(0)
                continue
            if (csv['min_rate'][i]>down and csv['max_rate'][i]<up):
                wrong_row_num.append(i)
            if (tup[1]==tup[2]==0):
                used.append(0)
            else:
                used.append(1)
            score+=calc(csv['min_rate'][i],csv['max_rate'][i],tup)
        else:
            used.append(0)
    print(score,lis)
    global wrong
    wrong=csv.iloc[wrong_row_num]
    return score,lis
def save_wrong(csv_name):
    wrong.to_csv(csv_name+'_wrong.csv')
