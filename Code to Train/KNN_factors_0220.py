import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from jqdatasdk import *
from jqdatasdk import finance
from sklearn.neighbors import KNeighborsClassifier

df=get_money_flow('002458.XSHE',
        fields=['date','sec_code','change_pct','net_amount_main','net_pct_main']
        ,start_date='2018-04-09',end_date='2020-04-08')
df['up_or_down']=np.where(df['change_pct']>0,1,0)
df['money_in_out']=np.where(df['net_amount_main']>0,1,0)

df['factor_wa']=df['up_or_down']*df['money_in_out']
df['next_day']=df['up_or_down'].shift(-1)

dataset=df.drop(['date','sec_code','up_or_down','money_in_out'],axis=1)
X=dataset.drop(['next_day'],axis=1)[:-1]
y=dataset['next_day'][:-1]
X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=30)
knn=KNeighborsClassifier(n_neighbors=95)
knn.fit(X_train,y_train)
print(knn.score(X_train,y_train))
print(knn.score(X_test,y_test))
