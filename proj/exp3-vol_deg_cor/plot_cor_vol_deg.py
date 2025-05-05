#!/usr/bin/env python3

# input: 1) corr rank file for graph and 2) mean stock volume
import pandas as pd
import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import networkx as nx

parser = argparse.ArgumentParser(description='Plot Volume vs Degree')
parser.add_argument('--input', '-i', type=str, required=True, help='input rank file')
parser.add_argument('--volume_file', '-v', type=str, required=True, help='mean volume file')
parser.add_argument('--output', '-o', type=str, required=True, help='output plot file')

args = parser.parse_args()

def cor_deg_vol(df_cor, df_vol, m):
    '''
    df_cor: stock log return corrlation rank table
    '''
    if 'cor' not in df_cor.columns:
        raise ValueError('input looks like a correlation table, not a rank table. please provide a rank table instead')
    df_cor = df_cor.sort_values(by='cor', ascending=False) # sort by correlation
    g = nx.Graph()
    cors = []
    for i,row in df_cor.iterrows():
        ks = []
        vols = []
        if i == m:
            break
        sym1 = row['sym1']
        sym2 = row['sym2']
        g.add_edge(sym1,sym2)
        # get node degree and mean volume
        for u in g.nodes():
            k = g.degree(u)
            ks.append(k)
            vol = df_vol[df_vol['symbol'] == u]['volume'].values[0]
            assert type(vol) == type(np.float64(1)), f'volume is not np.float64: "{vol} (type: {type(vol)})"'
            vols.append(vol)
            if (k==0) or (vol == 0):
                print(f'node {u} has degree 0 or volume 0')
        # compute correlation
        if i == 0:
            continue
        cor = np.corrcoef(ks, vols)[0,1]
        cors.append(cor)
    return cors

m=1000
df_cor = pd.read_csv(args.input)
df_vol = pd.read_csv(args.volume_file)
cors = cor_deg_vol(df_cor, df_vol, m)

# line plot  cor over m
plt.plot(cors)
plt.xlabel('m')
plt.ylabel('Corrleation of degree and mean volume')
plt.ylim(-1, 1)
plt.hlines(y=0,xmin=0,xmax=m, color='black', linestyle='--', label='0 correlation')
plt.legend()
plt.grid(False)
plt.savefig(args.output)
plt.close()
