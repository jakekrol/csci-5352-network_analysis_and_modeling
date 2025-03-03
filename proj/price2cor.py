#!/usr/bin/env python3
import math
import pandas as pd
import sys

### data
# from https://www.kaggle.com/datasets/dgawlik/nyse
df = pd.read_csv('./prices-split-adjusted.csv')

### get intersection of dates for all symbols
# d = {}
# for i, symbol in enumerate(df['symbol'].unique()):
#     print(i,symbol)
#     # first symbol set
#     if i == 0:
#         x = df[df['symbol']==symbol]
#         A = set(x['date'].values)
#         print('# of dates',len(A))
#         d[symbol] = len(A)
#         continue
#     # other symbols
#     x = df[df['symbol']==symbol]
#     B = set(x['date'].values)
#     print('# of dates',len(B))
#     d[symbol] = len(B)
#     A = A.intersection(B)

# with open('dates.txt','w') as f:
#     for symbol, count in d.items():
#         f.write(symbol+' '+str(count)+'\n')

### intersection of dates
# print(len(A))
# l = list(A)
# l.sort()
# with open('dates.txt','w') as f:
#     for date in l:
#         f.write(date+'\n')

### symbols with 1762 dates
# grep 1762 dates.txt | cut -d' ' -f1 > symbols.txt
symbols = []
with open('symbols.txt','r') as f:
    for line in f:
        symbols.append(line.strip())
symbols.sort()

# print('df shape', df.shape)
# df = df[df['symbol'].isin(symbols)]
# print('df_sub shape', df.shape)

### get intersection of dates for subset of symbols
# d = {}
# for i, symbol in enumerate(symbols):
#     print(i,symbol)
#     # first symbol set
#     if i == 0:
#         x = df_sub[df_sub['symbol']==symbol]
#         A = set(x['date'].values)
#         print('# of dates',len(A))
#         d[symbol] = len(A)
#         continue
#     # other symbols
#     x = df_sub[df_sub['symbol']==symbol]
#     B = set(x['date'].values)
#     print('# of dates',len(B))
#     d[symbol] = len(B)
#     A = A.intersection(B)

# print(len(A))
# l = list(A)
# l.sort()
# with open('dates_sub.txt','w') as f:
#     for date in l:
#         f.write(date+'\n')
### result
# this produced a set of 1762 dates
# all shared by the subset of symbols


### set log return (the difference of log closing price between two days)
def log_ret(t1,t0):
    return math.log(t1) - math.log(t0)
# sort symbols by date
df = df.sort_values(['symbol','date'])
d_return = {}
for sym in symbols:
    d_return[sym] = []
for sym in symbols:
    print('symbol',sym)
    # reset index to access previous row/date
    d = df[df['symbol']==sym].reset_index() 
    for i in d.index:
        # no previous closeprice
        if i == 0:
            continue
        date = d.loc[i,'date']
        # calculate log return
        t0 = d.loc[i-1,'close']
        t1 = d.loc[i,'close']
        diff = log_ret(t1,t0)
        d_return[sym].append(diff)
# convert to datafraem
df_return = pd.DataFrame(d_return)
df_return.to_csv('log_return.csv', index=False)

### correlation of log return vectors
df_return = pd.read_csv('log_return.csv')
print(df_return.columns)
cor = df_return.corr(method='pearson')
print(cor)
cor.to_csv('correlation.csv')




