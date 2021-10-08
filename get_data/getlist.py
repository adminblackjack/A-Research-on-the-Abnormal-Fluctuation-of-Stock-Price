import pandas as pd

all_stocks_dataframe=pd.read_csv('股票列表.csv',encoding='gbk')
length=len(all_stocks_dataframe['id'])

js=0
today='2021-10-08'
for i in range(0,length):
    #删除创业板
    s=all_stocks_dataframe['id'][i]
    if (s[:3]=="300"):
        all_stocks_dataframe.drop([i],inplace=True)
        continue
    #删除退市股
    end_date=all_stocks_dataframe['end_date'][i]
    if (end_date<today):
        js+=1
        all_stocks_dataframe.drop([i],inplace=True)
        continue
    start_date=all_stocks_dataframe['start_date'][i]
    year=start_date[:4]
    if (year>='2020'):
        all_stocks_dataframe.drop([i],inplace=True)
        continue

print(js)
print(all_stocks_dataframe.info())
all_stocks_dataframe.to_csv("删除.csv",encoding="gbk")
