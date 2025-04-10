#!/usr/bin/env python3
import pandas as pd
import heapq
import sys,os
import numpy as np
import math
import argparse

parser = argparse.ArgumentParser(description='Correlation to Rank')
parser.add_argument('--input', '-i', type=str, required=True, help='input correlation matrix file')
parser.add_argument('--timestep', '-t', type=int, default=1, help='timestep for log return calculation')
parser.add_argument('--output', '-o', type=str, help='output file name')
args = parser.parse_args()

df = pd.read_csv(args.input, index_col=0)

k=math.comb(df.shape[0],2)
hq = []
for i in range(df.shape[0]):
    for j in range(i+1,df.shape[1]):
        sym_i = df.index[i]
        sym_j = df.columns[j]
        cor = df.iloc[i,j]
        if len(hq) < k:
            heapq.heappush(hq, (sym_i,sym_j,cor)) # push element to heap
        else:
            if cor > hq[0][2]:
                heapq.heapreplace(hq, (sym_i,sym_j,cor)) # replace smallest element in heap
topk= sorted(hq,reverse=True, key=lambda x: x[2])
df = pd.DataFrame(topk,columns=['sym1','sym2','cor'])
df.to_csv(f'{args.output}',index=False)
