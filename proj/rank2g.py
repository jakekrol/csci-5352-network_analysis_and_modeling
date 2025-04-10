#!/usr/bin/env python3
# input rank file
# output graph

import os,sys
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pyvis.network import Network
import argparse
import numpy as np
import itertools
import random

parser = argparse.ArgumentParser(description='Rank to Graph')
parser.add_argument('--input', '-i', type=str, required=True, help='input rank file')
parser.add_argument('--m', '-m', type=int, required=True, help='number of edges')
parser.add_argument('--rand', '-r', action='store_true', help='randomize edges')
parser.add_argument('--plot', '-p', action='store_true', help='plot graph')
parser.add_argument('--out', '-o', type=str, required=True, help='output pattern')
parser.add_argument('--steps', '-s', type=str, help='comma-separated set of edge integers to plot at')
args = parser.parse_args()

# meta
SYMBOLS = '/home/jake/ghub/csci-5352-network_analysis_and_modeling/proj/symbols.txt'
NODE_META='/home/jake/ghub/csci-5352-network_analysis_and_modeling/proj/securities.csv'
df_node_meta = pd.read_csv(NODE_META)

# steps
if args.steps:
    args.steps = set(args.steps.split(','))
    args.steps = {int(i) for i in args.steps}

# print parsed args
print('# args')
print('input',args.input)
print('m',args.m)
print('rand',args.rand)
print('out',args.out)
print('steps',args.steps)

# cmap
colors = [
    "lightred",
    "lightblue",
    "green",
    "orange",
    "cyan",
    "magenta",
    "yellow",
    "brown",
    "pink",
    "lime",
    "teal",
    "gray"
]

values = [
    "Consumer Discretionary",
    "Consumer Staples",
    "Energy",
    "Financials",
    "Health Care",
    "Industrials",
    "Information Technology",
    "Materials",
    "Real Estate",
    "reports",
    "Telecommunications Services",
    "Utilities"
]
cmap = dict(zip(values, colors))


### f
def get_node_meta(symbol,df_node_meta=df_node_meta):
    d={}
    try:
        row = df_node_meta[df_node_meta['Ticker symbol'] == symbol]
    except KeyError as e:
        print(e)
        print(f'symbol " {symbol} " not found in node meta')
        return {'sector': None,'subsector':None,'location':None}
    sect = row['GICS Sector'].values[0]
    subsect = row['GICS Sub Industry'].values[0]
    location = row['Address of Headquarters'].values[0]
    d['sector'] = sect
    d['subsector'] = subsect
    d['location'] = location
    return d
def plotg(g, out, color=False):
    if color:
        sectors_present = set()
        for node in g.nodes():
            sector = g.nodes[node]['sector']
            if sector in cmap.keys():
                g.nodes[node]['color'] = cmap[sector]
            else:
                g.nodes[node]['color'] = 'black'
            sectors_present.add(sector)
    net = Network(notebook=False)
    net.from_nx(g)
    net.write_html(out)
    # append html with the cmap
    with open(out, "a") as file:
        # filter cmap to only include sectors present in the graph
        cmap_filtered = {k: v for k, v in cmap.items() if k in sectors_present}
        # make the text bigger
        file.write(f"<style>p {{ font-size: 20px; }}</style>\n")
        file.write(f"<p>{cmap_filtered}</p>\n")  # Wrap the dictionary in a <p> tag

def rank2g(df, m, output_pattern, steps):
    if 'cor' not in df.columns:
        raise ValueError('input looks like a correlation table, not a rank table. please provide a rank table instead')
    df = df.sort_values(by='cor', ascending=False) # sort by correlation
    g = nx.Graph()
    ms = []
    mean_degs = []
    Cs = []
    n_lccs = []
    diameters = []
    n_comp=[]
    mods=[]
    partition = {k:set() for k in cmap.keys()}
    for i,row in df.iterrows():
        if i == m:
            break
        sym1 = row['sym1']
        sym2 = row['sym2']
        # nodes
        if not g.has_node(sym1):
            d = get_node_meta(sym1)
            g.add_node(sym1)
            for key in d:
                g.nodes[sym1][key] = d[key]
                if key == 'sector':
                    sector = d[key]
                    partition[sector].add(sym1)
        if not g.has_node(sym2):
            d = get_node_meta(sym2)
            g.add_node(sym2)
            for key in d:
                g.nodes[sym2][key] = d[key]
                if key == 'sector':
                    sector = d[key]
                    partition[sector].add(sym2)
        # do list of sets instead of dict
        p = []
        for k,v in partition.items():
            if len(v) > 0:
                p.append(v)
        # edges
        cor = row['cor']
        g.add_edge(sym1,sym2, weight = cor)
        # compute statistics
        mean_deg = sum(dict(g.degree()).values()) / g.number_of_nodes()
        C = nx.transitivity(g)
        lcc = max(nx.connected_components(g), key=len)
        n_lcc = len(lcc)
        n_components = nx.number_connected_components(g)
        # diameter w.r.t largest connected component
        if n_lcc > 1:
            diameter = nx.diameter(g.subgraph(lcc))
        else:
            diameter = 0
        mod = nx.community.modularity(g, p)
        ms.append(i+1)
        mean_degs.append(mean_deg)
        Cs.append(C)
        n_lccs.append(n_lcc)
        diameters.append(diameter)
        n_comp.append(n_components)
        mods.append(mod)
        # plot
        if args.plot:
            if i+1 in steps:
                # plot graph
                print(f'plotting graph at {i+1} edges')
                plotg(g,f'{output_pattern}_e{i+1}.html', color=True)
        print(i)
    stats = pd.DataFrame(
        {'m':ms,'mean_deg':mean_degs,'C':Cs,'n_lcc':n_lccs,'diameter':diameters,
         'n_comp':n_comp,'modularity':mods})
    return g, stats

def cor2g_rand(df, m, output_pattern, steps, seed = 0):
    if 'cor' in df.columns:
        raise ValueError('input looks like a rank table, not a correlation table. please provide a correlation table instead')
    random.seed(seed)
    symbols = sorted(list(df.index)) # sorting ensures combinations are in same order for different runs
    comb = list(itertools.combinations(symbols, 2)) # symbols combinations
    print(comb[:5])
    g = nx.Graph()
    ms = []
    mean_degs = []
    Cs = []
    n_lccs = []
    diameters = []
    n_comp = []
    mods=[]
    partition = {k:set() for k in cmap.keys()}
    for i in range(m):
        if i == m:
            break
        sym1, sym2 = random.choice(comb) # sample symbols
        comb.remove((sym1, sym2)) # rm symbol from consideration
        # nodes
        if not g.has_node(sym1):
            d = get_node_meta(sym1)
            g.add_node(sym1)
            for key in d:
                g.nodes[sym1][key] = d[key]
                if key == 'sector':
                    sector = d[key]
                    partition[sector].add(sym1)
        if not g.has_node(sym2):
            d = get_node_meta(sym2)
            g.add_node(sym2)
            for key in d:
                g.nodes[sym2][key] = d[key]
                if key == 'sector':
                    sector = d[key]
                    partition[sector].add(sym2)
        # do list of sets instead of dict
        p = []
        for k,v in partition.items():
            if len(v) > 0:
                p.append(v)
        # edges
        cor = df.loc[sym1,sym2]
        g.add_edge(sym1,sym2, weight = cor)
        # compute statistics
        mean_deg = sum(dict(g.degree()).values()) / g.number_of_nodes()
        C = nx.transitivity(g)
        lcc = max(nx.connected_components(g), key=len)
        n_lcc = len(lcc)
        n_components = nx.number_connected_components(g)
        # diameter w.r.t largest connected component
        if n_lcc > 1:
            diameter = nx.diameter(g.subgraph(lcc))
        else:
            diameter = 0
        mod = nx.community.modularity(g, p)
        ms.append(i+1)
        mean_degs.append(mean_deg)
        Cs.append(C)
        n_lccs.append(n_lcc)
        diameters.append(diameter)
        n_comp.append(n_components)
        mods.append(mod)
        # plot
        if args.plot:
            if i+1 in steps:
                # plot graph
                print(f'plotting graph at {i+1} edges')
                plotg(g,f'{output_pattern}_e{i+1}.html', color=True)
        print(i)
    stats = pd.DataFrame({'m':ms,'mean_deg':mean_degs,'C':Cs,'n_lcc':n_lccs,'diameter':diameters,
                          'n_comp':n_comp,'modularity':mods})
    return g, stats

def main():
    # set node communities by sector
    # partition={k:[] for k in cmap.keys()} 
    # with open(SYMBOLS) as f:
    #     for line in f:
    #         s = line.strip()
    #         sector = get_node_meta(s)['sector']
    #         if sector in cmap.keys():
    #             partition[sector].append(s)
    #         else:
    #             raise ValueError(f'symbol {s} not found in cmap')
    # graphs
    if args.rand:
        df = pd.read_csv(args.input, index_col=0) # read corr
        print('generating random graphs')
        _, stats = cor2g_rand(df, args.m, args.out, args.steps)
        stats.to_csv(f'{args.out}_stats.tsv', index=False, sep ='\t')
    else:
        df = pd.read_csv(args.input) # read rank
        print('generating graphs')
        _, stats = rank2g(df, args.m, args.out, args.steps)
        stats.to_csv(f'{args.out}_stats.tsv', index=False, sep ='\t')
    print('done')
main()



