import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('601318.XSHG_new.csv')

def classification_tc(data):
    data['open-close']=data['open']-data['close']
    data['high-low']=data['high']-df['low']
    data['target']=np.where(data['close'].shift(-1)>data['close'],1,-1)
    X=data[['open-close','high-low']]
    y=data['target']
    return (X,y)

def regression_tc(data):
    data['open-close']=data['open']-data['close']
#    data['open-close']=np.where(data['open']-data['close']==0,0.01,data['open']-data['close'])
    data['high-low']=data['high']-data['low']
    data['target']=data['close'].shift(-1)-df['close']
#    data=data.dropna()
    X=data[['open-close','high-low']]
    data['target'][938]=0
    y=data['target']
    return (X,y)

'''
X,y=classification_tc(df)
X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=0.8)
knn_clf=KNeighborsClassifier(n_neighbors=30)
knn_clf.fit(X_train,y_train)
print(knn_clf.score(X_train,y_train))
print(knn_clf.score(X_test,y_test))
'''

X,y=regression_tc(df)
X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=0.8)
knn_reg=KNeighborsRegressor(n_neighbors=30)
#X_train.to_csv('tempx.csv')
#y_train.to_csv('tempy.csv')
knn_reg.fit(X_train,y_train)
df['predict_signal']=knn_reg.predict(X)
df['return']=np.log(df['close']/df['close'].shift(1))
print(df.head())

def cum_return(data,split_value):
    cum_return=data[split_value:]['return'].cumsum()*100
    return cum_return

def strategy_return(data,split_value):
    data['strategy_return']=data['return']*data['predict_signal'].shift(1)
    cum_strategy_return=data[split_value:]['strategy_return'].cumsum()*100
    return cum_strategy_return

def plot_chart(cum_return,cum_strategy_return,symbol):
    plt.figure(figsize=(90,60))
    plt.plot(cum_return,'--',label='%s Returns'%symbol)
    plt.plot(cum_strategy_return,label='Strategy Returns')
    plt.legend()
    plt.show()

cum_return=cum_return(df,split_value=len(X_train))
cum_strategy_return=strategy_return(df,split_value=len(X_train))
plot_chart(cum_return,cum_strategy_return,'zgpa')
