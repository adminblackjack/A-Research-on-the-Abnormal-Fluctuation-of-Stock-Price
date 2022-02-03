import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from jqdatasdk import *
from jqdatasdk import finance
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import datetime

stocks=get_index_stocks('000016.XSHG')
q=query(valuation.code,
        valuation.market_cap,
        balance.total_assets-balance.total_liability,
        balance.total_assets/balance.total_liability,
        income.net_profit,
        indicator.inc_revenue_year_on_year,
        balance.development_expenditure
        ).filter(valuation.code.in_(stocks))
df=get_fundamentals(q)
df.columns=['code',
        'mcap',
        'na',
        '1/DA ratio',
        'net income',
        'growth',
        'RD']
print(df.head())
df.index=df['code'].values
df=df.drop('code',axis=1)
X=df.drop('mcap',axis=1)
y=df['mcap']
X=X.fillna(0)
y=y.fillna(0)
reg=LinearRegression().fit(X,y)
predict=pd.DataFrame(reg.predict(X),index=y.index,columns=['predict_mcap'])
print(predict.head())
diff=df['mcap']-predict['predict_mcap']
diff=df.DataFrame(diff,index=y.index,columns=['diff'])
diff=diff.sprt_value(by='diff',ascending=True)
print(diff.head(8))

