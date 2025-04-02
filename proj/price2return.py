#!/usr/bin/env python3
import math
import pandas as pd
import sys
import argparse

parser = argparse.ArgumentParser(description='Calculate log return of stock prices')
parser.add_argument('--prices', '-p', type=str, required=True, help='input stock prices file')
parser.add_argument('--symbols', '-s', type=str, required=True, help='input symbols file')
parser.add_argument('--timestep', '-t', type=int, default=1, help='timestep for log return calculation')
args = parser.parse_args()

### data
# from https://www.kaggle.com/datasets/dgawlik/nyse
df = pd.read_csv(args.prices)
symbols = []
# see price2cor.py for symbols.txt generation
with open(args.symbols,'r') as f:
    for line in f:
        symbols.append(line.strip())
symbols.sort()

### set log return (the difference of log closing price between two days)
def log_ret(t1,t0):
    return math.log(t1) - math.log(t0)

# sort symbols by date
df = df.sort_values(['symbol','date'])
T = df['date'].nunique() # number of unique dates
print('T initial',T)    
T_floor = math.floor(T/args.timestep) # floor to ensure interval is always satisfied
print('floor(T/t)',T_floor)

def get_date_index(T,t):
    idxs = []
    i = 0
    while i <= T-1:
        idxs.append(i)
        i+=t
    return idxs
# get index of dates
idx_dates = get_date_index(T,args.timestep)
print('idx_dates',idx_dates)

# test
# print('test')
# for sym in symbols: # only consider the symbols with shared dates
#     df_sym = df[df['symbol']==sym].reset_index()
#     for i in idx_dates:
#         with open ('test.txt','a') as f:
#             date = df_sym.loc[i,'date']
#             symbol = df_sym.loc[i,'symbol']
#             close = df_sym.loc[i,'close']
#             f.write(f'{date} {symbol} {close}\n')
# sys.exit()



d_return = {}
for sym in symbols:
    d_return[sym] = []
for sym in symbols:
    print('symbol',sym)
    # reset index to access previous row/date
    df_sym = df[df['symbol']==sym].reset_index() 
    for j,i in enumerate(idx_dates):
        # no previous closeprice
        if i == 0:
            continue
        # calculate log return
        t0 = df_sym.loc[idx_dates[j-1],'close']
        t1 = df_sym.loc[i,'close']
        diff = log_ret(t1,t0)
        d_return[sym].append(diff)
# convert to datafraem
df_return = pd.DataFrame(d_return)
df_return.to_csv(f'log_return_{args.timestep}.csv', index=False)

### correlation of log return vectors
# df_return = pd.read_csv('log_return.csv')
df_return = pd.read_csv(f'log_return_{args.timestep}.csv')
print(df_return.columns)
cor = df_return.corr(method='pearson')
print(cor)
# cor.to_csv('correlation.csv')
cor.to_csv(f'correlation_{args.timestep}.csv')




