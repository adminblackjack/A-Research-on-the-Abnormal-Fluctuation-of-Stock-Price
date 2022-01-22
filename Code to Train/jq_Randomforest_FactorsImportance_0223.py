import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from jqdatasdk import *
from jqdatasdk import finance
from sklearn.tree import DecisionTreeRegressor
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import datetime
from jqdatasdk.technical_analysis import *
from sklearn.tree import DecisionTreeClassifier

'''
X,y=make_regression(n_samples=100,n_features=1,noise=60,random_state=18)
plt.scatter(X,y,s=80,c=y,edgecolor='grey',alpha=0.6)
plt.grid()
plt.show()
'''

'''
reg=DecisionTreeRegressor(max_depth=None)
reg.fit(X,y)
X_new=np.linspace(-2.5,3.5,100)
y_new=reg.predict(X_new.reshape(-1,1))
plt.scatter(X,y,s=80,
        c=y,edgecolor='grey',
        alpha=0.4)
plt.plot(X_new,y_new,lw=2,
        ls='-',c='grey')
plt.grid()
'''

stocks=get_index_stocks('000300.XSHG')
q=query(valuation.code,valuation.market_cap,
        balance.total_current_assets-balance.total_current_liability,
        balance.total_liability-balance.total_assets,
        balance.total_liability/balance.equities_parent_company_owners,
        (balance.total_assets-balance.total_current_assets)/balance.total_assets,
        balance.equities_parent_company_owners/balance.total_assets,
        indicator.inc_total_revenue_year_on_year,
        valuation.turnover_ratio,
        valuation.pe_ratio,
        valuation.pb_ratio,
        valuation.ps_ratio,indicator.roa).filter(
                valuation.code.in_(stocks))
df=get_fundamentals(q,date=None)
df.columns=['code','市值','净营运资本','净债务','产权比率',
        '非流动资产比率','股东权益比率','营收增长率','换手率','PE','PB','PS','总资产收益率']
print(df.head())

df.index=df.code.values
del df['code']
today=datetime.datetime.today()
delta50=datetime.timedelta(days=50)
delta1=datetime.timedelta(days=1)
delta2=datetime.timedelta(days=2)
history=today-delta50
yesterday=today-delta1
two_days_ago=today-delta2
df['动量线']=list(MTM(list(df.index),two_days_ago,timeperiod=10,
    unit='1d',include_now=True).values())
df['成交量']=list(VOL(list(df.index),two_days_ago,M1=10,
    unit='1d',include_now=True)[0].values())
df['累计能量线']=list(OBV(list(df.index),check_date=two_days_ago,
    timeperiod=10).values())
df['平均差']=list(DMA(list(df.index),two_days_ago,N1=10,unit='1d',
    include_now=True)[0].values())
df['指数移动平均']=list(EMA(list(df.index),two_days_ago,timeperiod=10,
    unit='1d',include_now=True).values())
df['移动平均']=list(MA(list(df.index),two_days_ago,timeperiod=10,
    unit='1d',include_now=True).values())
df['乖离率']=list(BIAS(list(df.index),two_days_ago,N1=10,unit='1d',include_now=True)[0].values())
df.fillna(0,inplace=True)
print(df.head())

df['close1']=list(get_price(stocks,
    end_date=yesterday,count=1,fq='pre',panel=False)['close'])
df['close2']=list(get_price(stocks,
    end_date=history,count=1,fq='pre',panel=False)['close'])
df['return']=df['close1']/df['close2']-1
df['signal']=np.where(df['return']<df['return'].mean(),0,1)
print(df.head())

X=df.drop(['close1','close2','return','signal'],axis=1)
y=df['signal']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
clf=DecisionTreeClassifier(random_state=1000)
clf.fit(X_train,y_train)
print(clf.score(X_train,y_train))
print(clf.score(X_test,y_test))

factor_weight=pd.DataFrame({'features':list(X.columns),'importance':
    clf.feature_importances_}).sort_values(by='importance',ascending=False)
print(factor_weight)
