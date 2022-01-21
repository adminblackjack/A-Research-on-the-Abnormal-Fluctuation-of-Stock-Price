import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from jqdatasdk import *
from jqdatasdk import finance
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

indices=get_all_securities(types=['index'])
indices.head(10)
factor_mc=get_factor_values(securities=get_index_stocks('000300.XSHG'),
        factors=['market_cap'],end_date='2020-04-10',count=1)['market_cap']
print(factor_mc.T.head())
factor_cfp=get_factor_values(securities=get_index_stocks('000300.XSHG'),
        factors=['cash_flow_to_price_ratio'],
        end_date='2020-04-10',
        count=1)['cash_flow_to_price_ratio']
print(factor_cfp.T.head(5))
factor_npr=get_factor_values(securities=get_index_stocks('000300.XSHG'),
        factors=['net_profit_ratio'],
        end_date='2020-04-10',
        count=1)['net_profit_ratio']
print(factor_npr.T.head())
factor_npgr=get_factor_values(securities=get_index_stocks('000300.XSHG'),
        factors=['net_profit_growth_rate'],
        end_date='2020-04-10',
        count=1)['net_profit_growth_rate']
print(factor_npgr.T.head())
factors=pd.DataFrame(index=factor_mc.T.index)
factors['mc']=factor_mc.T['2020-04-10 00:00:00']
factors['cfp']=factor_cfp.T['2020-04-10 00:00:00']
factors['npf']=factor_npr.T['2020-04-10 00:00:00']
factors['npgr']=factor_npgr.T['2020-04-10 00:00:00']
print(factors.head())
factors=factors.dropna()
print(factors.isnull().sum())
scaler=StandardScaler()
factors_scl=scaler.fit_transform(factors)
pca=PCA(n_components=1)#提取主成分数量为1
pca.fit(factors_scl)
print(pca.components_)
factors['pca']=pca.transform(factors_scl)
print(factors.sort_values(by='pca',ascending=False).head())
