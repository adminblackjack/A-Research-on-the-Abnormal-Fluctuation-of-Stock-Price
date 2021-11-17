import rqdatac
import os
import csv
import pandas as pd
import time

rqdatac.init()


path=os.getcwd()
L=list(path)
for i in range(0,len(L)):
    if (L[i]=="\\"):
        L[i]='/'
path=''.join(L)
os.chdir(path+"/all_stocks")
all_stocks=pd.read_csv("all_stocks.csv",encoding="GB18030")
N=None
cnt=0
length=len(all_stocks['id'])
for i in range(0,length):
    if (all_stocks['end_date'][i]<="2016-03-01"):
        continue
    index=all_stocks['id'][i]
    if ('600848') in index:
        cnt+=1
        continue
    if (cnt==0):
        continue
    value=rqdatac.get_price(index,start_date=20160301,end_date=20191231)
    print(type(value))
    if (type(value)==type(N)):
        continue
    os.chdir(path)
    os.makedirs(path+"/"+index)
    os.chdir(path+"/"+index)
    value.to_csv(index+".csv")
