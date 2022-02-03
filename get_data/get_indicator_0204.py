import pandas as pd
import numpy as np
from jqdatasdk import *
from matplotlib import pyplot as plt
import os
import talib
import ta.volume
from jqdatasdk import finance

def query_spare():
    # 判断当日查询条数余额
    spare = get_query_count()['spare']
    if spare < 50000:
        print('spare',spare)
        sys.exit()
    return spare
print(query_spare())
def process(code):
    save=pd.read_csv(code+'_new.csv')
    if (len(save)<80):
        return False
    if (str(get_security_info(code).end_date)<'2021-12-30'):
        return False

    q=query(valuation.capitalization).filter(valuation.code==code)
    temp=get_fundamentals(q,date='2021-12-30')
    save['turnover_rate']=save['volume']/(temp.iloc[-1]['capitalization']*10000)*100

    #WMA
    price_WMA5=talib.WMA(save['close'],timeperiod=5)
    price_WMA15=talib.WMA(save['close'],timeperiod=15)
    price_WMA50=talib.WMA(save['close'],timeperiod=50)

    #TSI
    N,M=25,13
    price_TSI=talib.EMA(talib.EMA(save['close']-save['close'].shift(1),N),M)/talib.EMA(talib.EMA(abs(save['close']-save['close'].shift(1)),N),M)
    price_TSI*=100

    #BIAS
    N,M=3,20
    price_BIAS=100*(talib.EMA(save['close'],N)-talib.MA(save['close'],M))/talib.MA(
        save['close'],M)

    #NATR
    price_NATR=talib.NATR(save['high'],save['low'],save['close'],timeperiod=10)
    #momentum

    #TRIX
    mom_TRIX=talib.TRIX(save['close'],timeperiod=24)

    #CCI
    mom_CCI=talib.CCI(save['high'],save['low'],save['close'],timeperiod=15)

    #volume

    #WMA
    vol_WMA3=talib.WMA(save['volume'],timeperiod=3)
    vol_WMA15=talib.WMA(save['volume'],timeperiod=15)

    #MFI
    vol_MFI=talib.MFI(save['high'],save['low'],save['close'],save['volume'],timeperiod=10)

    #CMF
    vol_CMF=ta.volume.chaikin_money_flow(save['high'],save['low'],save['close'],save['volume'])

    #BIAS
    N,M=3,15
    vol_BIAS=100*(talib.EMA(save['volume'],N)-talib.MA(save['volume'],M))/talib.MA(
        save['volume'],M)

    price_type=[]

    for i in range(0,len(save)):
        #天地板且收盘跌停-5,一字跌停-4，开盘跌停-3，收盘仍然跌停-2,盘中存在跌停-1
        #一般0,盘中存在涨停1,收盘仍然涨停2,开盘涨停3,一字涨停4,地天板且收盘涨停5
        price_type.append(0)
        if (save['high'][i]==save['limit_up'][i] and save['open'][i]!=save['limit_up'][i]):
            price_type[i]=1
        if (save['high'][i]==save['limit_up'][i] and save['open'][i]!=save['limit_up'][i]
            and save['close'][i]==save['limit_up'][i]):
            price_type[i]=2
        if (save['high'][i]==save['limit_up'][i] and save['open'][i]==save['limit_up'][i]):
            price_type[i]=3
        if (save['low'][i]==save['high'][i]==save['limit_up'][i]):
            price_type[i]=4
        if (save['high'][i]==save['limit_up'][i] and save['low'][i]==save['limit_down'][i] and
            save['close'][i]==save['limit_up'][i]):
            price_type[i]=5
        if (save['low'][i]==save['limit_down'][i] and save['open'][i]!=save['limit_down'][i]):
            price_type[i]=-1
        if (save['low'][i]==save['limit_down'][i] and save['open'][i]!=save['limit_down'][i]
            and save['close'][i]==save['limit_down'][i]):
            price_type[i]=-2
        if (save['high'][i]==save['limit_down'][i] and save['open'][i]==save['limit_down'][i]):
            price_type[i]=-3
        if (save['low'][i]==save['high'][i]==save['limit_down'][i]):
            price_type[i]=-4
        if (save['high'][i]==save['limit_up'][i] and save['low'][i]==save['limit_down'][i] and
            save['close'][i]==save['limit_down'][i]):
            price_type[i]=-5

    price_type=pd.Series(price_type,index=range(len(price_type)))
    price_type.to_csv('new.csv')
    save['price_type']=price_type
    need=[
        ('price_WMA5',price_WMA5),
        ('price_WMA15',price_WMA15),
        ('price_WMA50',price_WMA50),
        ('price_TSI',price_TSI),
        ('price_BIAS',price_BIAS),
        ('price_NATR',price_NATR),
        ('mom_TRIX',mom_TRIX),
        ('mom_CCI',mom_CCI),
        ('vol_WMA3',vol_WMA3),
        ('vol_WMA15',vol_WMA15),
        ('vol_MFI',vol_MFI),
        ('vol_CMF',vol_CMF),
        ('vol_BIAS',vol_BIAS)]
    for name,VAR in need:
        save[name]=VAR
    save.to_csv(code+'_indicator_0204.csv')

    return True
os.chdir('/home/blackjack/rq/2016-2019-data')
path='/home/blackjack/rq/2016-2019-data'
listdir=os.listdir()
done=[]
drop=[]
cnt=0
for code in listdir:
    if (code[0]>'9' or code[0]<'0'):
        continue
    if (query_spare()<1000):
        break
    os.chdir(path+'/'+code)
    if (process(code)):
        print(code)
        done.append(code)
    else:
        drop.append(code)
    cnt+=1
    print(cnt)
drop=pd.Series(drop,index=range(len(drop)))
os.chdir('/home/blackjack/rq/2016-2019-data')
drop.to_csv('drop.csv')
