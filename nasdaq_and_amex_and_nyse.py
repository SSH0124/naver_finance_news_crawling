import FinanceDataReader as fdr
import pandas as pd

nasdaq = fdr.StockListing('NASDAQ')
amex = fdr.StockListing('AMEX')
nyse = fdr.StockListing('NYSE')

df2 = pd.concat([nasdaq, amex, nyse])
df = pd.concat([nasdaq, amex])
df1 = df.copy()
df1 = df1.drop_duplicates('Symbol')

nasdaq['Indexes']='NASDAQ'
print('나스닥', nasdaq.shape)

amex['Indexes']='AMEX'
print('아멕스', amex.shape)

nyse['Indexes']='NYSE'
print('뉴욕', nasdaq.shape)

print(df1.shape)
df_tail_1000 = df1.tail(1000)
df_tail_1000.to_csv('mini_stock.csv', index=False)
print(df2)
df2.to_csv('all_stock_industry.csv', index=False, encoding='cp949')
