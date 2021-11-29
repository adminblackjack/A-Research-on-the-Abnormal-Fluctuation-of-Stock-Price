import pandas as pd
import numpy as np
import pandas as pd

csv=pd.read_csv('all_stocks.csv',encoding="GB18030")
l=len(csv['end_date'])
for i in range(0,l):
    start_date=csv['start_date'][i]
    end_date=csv['end_date'][i]
    if (start_date[:4]>'2019' or end_date[:4]<='2019'):
        csv.drop(i,axis=0,inplace=True)

csv.to_csv('all_stocks_clean.csv')
