import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from jqdatasdk import *
from jqdatasdk import finance

'''
df=get_price('601318.XSHG',start_date='2020-01-01',end_date='2020-04-01',frequency='daily')
print(df.head())
'''
q=query(finance.STK_SHAREHOLDERS_SHARE_CHANGE.code,
        finance.STK_SHAREHOLDERS_SHARE_CHANGE.pub_date,
        finance.STK_SHAREHOLDERS_SHARE_CHANGE.type,
        finance.STK_SHAREHOLDERS_SHARE_CHANGE.change_number,
        finance.STK_SHAREHOLDERS_SHARE_CHANGE.change_ratio,
        finance.STK_SHAREHOLDERS_SHARE_CHANGE.after_change_ratio).filter(finance.STK_SHAREHOLDERS_SHARE_CHANGE.code=='002458.XSHE',
                finance.STK_SHAREHOLDERS_SHARE_CHANGE.pub_date>'2019-09-01')
'''
        finance.STK_SHAREHOLDER_TOP10.shareholder_rank,
        finance.STK_SHAREHOLDER_TOP10.shareholder_name,
        finance.STK_SHAREHOLDER_TOP10.shareholder_class,
        finance.STK_SHAREHOLDER_TOP10.share_ratio).filter(finance.STK_SHAREHOLDER_TOP10.code=='002458.XSHE',finance.STK_SHAREHOLDER_TOP10.pub_date>'2020-01-01')
'''
shareholders=finance.run_query(q)
print(shareholders)
