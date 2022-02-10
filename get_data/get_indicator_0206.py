import pandas as pd
import numpy as np
from jqdatasdk import *
from matplotlib import pyplot as plt
import os
import talib
import ta.volume
from jqdatasdk import finance
import dython
df=pd.read_csv("temp.csv")
df=df.dropna()
df=df.drop(['limit_down','limit_up','Unnamed: 0','date','low','high','open','order_book_id'],axis=1)
df.to_csv('drop.csv')
df=pd.read_csv("drop.csv")

df=(df.loc[:, ~df.columns.str.contains('^Unnamed')])
df=df.drop(['total_turnover'],axis=1)
#df=df.drop(['volume'],axis=1)

df=df.drop(['num_trades'],axis=1)
dython.nominal.associations(df,figsize=(20,10))
df.corr(method='kendall')
df.to_csv('drop.csv')
df['price_WMA5']=df['price_WMA5']/df['close']-1
df['price_WMA15']=df['price_WMA15']/df['close']-1
df['price_WMA50']=df['price_WMA50']/df['close']-1
df['price_TSI']/=100
df['price_BIAS']/=df['close']
df['vol_WMA3']/=df['volume']
df['vol_WMA15']/=df['volume']
df=df.drop(['volume'],axis=1)
df.to_csv('drop.csv')
