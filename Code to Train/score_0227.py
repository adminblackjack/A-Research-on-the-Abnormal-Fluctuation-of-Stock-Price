import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import math
csv=pd.read_csv('IsolationForest_Result_0227.csv')
csv=csv.loc[:,~csv.columns.str.contains("^Unnamed")]
csv.to_csv('IsolationForest_Result_0227.csv')
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
score=0
for i in range(0,len(csv)):
    score+=calc(csv['min_rate'][i],csv['max_rate'][i])
print(score)
print(lis)
