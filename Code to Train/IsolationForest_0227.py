import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from merlion.plot import plot_anoms
from merlion.utils import TimeSeries
#from ts_datasets.anomaly import NAB
import datetime
import time
import os
# Import models & configs
from merlion.models.anomaly.isolation_forest import IsolationForest, IsolationForestConfig
from merlion.models.anomaly.windstats import WindStats, WindStatsConfig
from merlion.models.anomaly.forecast_based.prophet import ProphetDetector, ProphetDetectorConfig

# Import a post-rule for thresholding
from merlion.post_process.threshold import AggregateAlarms

# Import a data processing transform
from merlion.transform.moving_average import DifferenceTransform
from merlion.evaluate.anomaly import TSADMetric
path=os.getcwd()
os.chdir(path+'/2016-2019-data')
path=os.getcwd()
drop=pd.read_csv('drop.csv')
drop=drop.loc[:,~drop.columns.str.contains("^Unnamed")]
lis=os.listdir()
config1 = IsolationForestConfig()
model1  = IsolationForest(config1)
total_score=0
total_num=0
print(path)
'''
def calc_score(k):
    maxrate=raw['max_rate'][k+250]
    minrate=raw['min_rate'][k+250]
    score=0
    if (0.7<minrate<0.8 and 1.3<maxrate<1.4):
        score
'''
result=pd.DataFrame(columns=('index','row_num','min_rate','min_days','max_rate','max_days'))
index=[]
row_num=[]
min_rate=[]
min_days=[]
max_rate=[]
max_days=[]
for i in range(0,len(lis)):
    if (lis[i][0]!='6' and lis[i][0]!='0' and lis[i][0]!='3'):
        continue
    if (lis[i] in drop['index']):
        continue
    os.chdir(path+'/'+lis[i])
    templis=os.listdir()
    if ((lis[i]+'_rate_0226.csv') not in templis):
        continue
    raw=pd.read_csv(lis[i]+'_rate_0226.csv')
    all_data=raw.loc[:,raw.columns.str.contains("turnover_rate")]
    if (len(all_data)<250):
        continue
    config1=IsolationForestConfig()
    model1=IsolationForest(config1)
#    train_size=int(0.4*len(all_data))
    train_size=250
    train=all_data[:train_size]
    train_data=TimeSeries.from_pd(train,freq='1d')
    test=all_data[train_size+1:]
    test_data=TimeSeries.from_pd(test,freq='1d')
    if (len(test)<2):
        continue
    train_scores_1=model1.train(train_data=train_data)
    labels_1=model1.get_anomaly_label(test_data)
    labels_1_df=labels_1.to_pd()
    print(lis[i])
    for j in range(0,len(labels_1_df)):
        if (labels_1_df['anom_score'][j]!=0):
#            print(1)
            index.append(lis[i])
            row_num.append(j+250)
            min_rate.append(raw['min_rate'][j+250])
            max_rate.append(raw['max_rate'][j+250])
            min_days.append(raw['min_days'][j+250])
            max_days.append(raw['max_days'][j+250])
result['index']=index
result['row_num']=row_num
result['min_rate']=min_rate
result['min_days']=min_days
result['max_rate']=max_rate
result['max_days']=max_days
print(result)
print(path)
os.chdir('/home/blackjack/rq')
result.to_csv('IsolationForest_Result_0227.csv')
