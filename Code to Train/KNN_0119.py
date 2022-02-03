import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('601318.XSHG_new.csv')
print(df.head())

def classification_tc(data):
    data['open-close']=data['open']-data['close']
    data['high-low']=data['high']-df['low']
    data['target']=np.where(data['close'].shift(-1)>data['close'],1,-1)
    X=data[['open-close','high-low']]
    y=data['target']
    return (X,y)

X,y=classification_tc(df)
X_train,X_test,y_train,y_test=train_test_split(X,y,train_size=0.8)
knn_clf=KNeighborsClassifier(n_neighbors=30)
knn_clf.fit(X_train,y_train)
print(knn_clf.score(X_train,y_train))
print(knn_clf.score(X_test,y_test))

