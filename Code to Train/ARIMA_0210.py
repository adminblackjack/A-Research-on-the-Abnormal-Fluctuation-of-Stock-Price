import pandas as pd
import numpy as np
import statsmodels as sm
import seaborn as sns
import matplotlib.pylab as plt
from scipy import stats

df=pd.read_csv('raw.csv')
df=df['volume']-df['volume'].shift(1)
df=df.dropna()
df=df/1e8
size=len(df)
n_train=int(size*0.8)+1
train=df.iloc[:n_train]
test=df.iloc[n_train+1:]
plt.plot(df)

from statsmodels.tsa.stattools import adfuller

print(adfuller(df,regression='ctt'))

from statsmodels.tsa.forecasting.stl import STLForecast
import statsmodels.api as sm

fig,axs=plt.subplots(2)
fig.tight_layout()
sm.graphics.tsa.plot_pacf(df,lags=20,ax=axs[0])
sm.graphics.tsa.plot_acf(df,lags=20,ax=axs[1])
train_results=sm.tsa.arma_order_select_ic(train,ic=['aic','bic','hqic'],trend='c',max_ar=5,max_ma=5)
print(train_results.bic_min_order)
order=(1,1)
ARMAmodel=sm.tsa.ARMA(df[:],order).fit()
plt.figure(figsize=(40,20))
plt.plot(df[:],'r',label='Raw')
plt.plot(ARMAmodel.fittedvalues,'g',label='ARMAmodel')
