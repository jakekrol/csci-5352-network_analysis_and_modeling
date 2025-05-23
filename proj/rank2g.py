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
import copy

parser = argparse.ArgumentParser(description='Rank to Graph')
parser.add_argument('--input', '-i', type=str, required=True, help='input rank file')
parser.add_argument('--m', '-m', type=int, required=True, help='number of edges')
parser.add_argument('--rand', '-r', action='store_true', help='randomize edges')
parser.add_argument('--plot', '-p', action='store_true', help='plot graph')
parser.add_argument('--out', '-o', type=str, required=True, help='output pattern')
parser.add_argument('--steps', '-s', type=str, help='comma-separated set of edge integers to plot at')
parser.add_argument('--keep', '-k', action='store_true', help='keep singleton nodes')
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
    try:
        sect = row['GICS Sector'].values[0]
    except IndexError as e:
        print(e)
        print(f'symbol " {symbol} " not found in node meta')
        sys.exit()
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

def g2stats(g, partition):
    # stats: mean degree, clustering coefficient, modularity, diameter, number of components, size LCC
    mean_deg = sum(dict(g.degree()).values()) / g.number_of_nodes()
    C = nx.transitivity(g)
    lcc = max(nx.connected_components(g), key=len)
    n_lcc = len(lcc)
    assert n_lcc > 0, 'lcc is empty'
    n_components = nx.number_connected_components(g)
    # diameter w.r.t largest connected component
    diameter = nx.diameter(g.subgraph(lcc))
    # just use the modularity from no --keep flag
    # it's the same
    # so is C, so we don't bother here
    if args.keep:
        mod = 0
    else:
        mod = nx.community.modularity(g, partition)
    return {'mean_deg':mean_deg, 'C':C, 'n_lcc':n_lcc, 'diameter':diameter, 'n_comp':n_components, 'modularity':mod}

def update_g(g, partition, sym1, sym2):
    '''
    add nodes with data, edge, and update partition
    '''
    g_p = g.copy()
    p = copy.deepcopy(partition)
    if not g_p.has_node(sym1):
        d = get_node_meta(sym1)
        g_p.add_node(sym1)
        for key in d:
            g_p.nodes[sym1][key] = d[key]
            if key == 'sector':
                sector = d[key]
                p[sector].add(sym1)
    if not g_p.has_node(sym2):
        d = get_node_meta(sym2)
        g_p.add_node(sym2)
        for key in d:
            g_p.nodes[sym2][key] = d[key]
            if key == 'sector':
                sector = d[key]
                p[sector].add(sym2)
    g_p.add_edge(sym1,sym2)
    return g_p, p


def rank2g(df, m, output_pattern, steps):
    if 'cor' not in df.columns:
        raise ValueError('input looks like a correlation table, not a rank table. please provide a rank table instead')
    # add all nodes
    if args.keep:
        # add all nodes to graph
        nodes = set()
        for i,row in df.iterrows():
            nodes.add(row['sym1'])
            nodes.add(row['sym2'])
        g = nx.Graph()
        for node in nodes:
            d = get_node_meta(node)
            g.add_node(node)
            for key in d:
                g.nodes[node][key] = d[key]
    else:
        g = nx.Graph()
    df = df.sort_values(by='cor', ascending=False) # sort by correlation
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
        g, partition = update_g(g, partition, sym1, sym2)
        # do list of sets instead of dict for modularity computation
        p = []
        for k,v in partition.items():
            if len(v) > 0:
                p.append(v)
        # compute statistics
        stats = g2stats(g, p)
        ms.append(i+1)
        mean_degs.append(stats['mean_deg'])
        Cs.append(stats['C'])
        n_lccs.append(stats['n_lcc'])
        diameters.append(stats['diameter'])
        n_comp.append(stats['n_comp'])
        mods.append(stats['modularity'])
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
    if args.keep:
        # add all nodes to graph
        nodes = set()
        for u in df.index:
            nodes.add(u)
        g = nx.Graph()
        for node in nodes:
            d = get_node_meta(node)
            g.add_node(node)
            for key in d:
                g.nodes[node][key] = d[key]
    else:
        g = nx.Graph()
    random.seed(seed)
    symbols = sorted(list(df.index)) # sorting ensures combinations are in same order for different runs
    comb = list(itertools.combinations(symbols, 2)) # symbols combinations
    print(comb[:5])
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
        g, partition = update_g(g, partition, sym1, sym2)
        # do list of sets instead of dict
        p = []
        for k,v in partition.items():
            if len(v) > 0:
                p.append(v)
        # compute statistics
        stats = g2stats(g, p)
        ms.append(i+1)
        mean_degs.append(stats['mean_deg'])
        Cs.append(stats['C'])
        n_lccs.append(stats['n_lcc'])
        diameters.append(stats['diameter'])
        n_comp.append(stats['n_comp'])
        mods.append(stats['modularity'])
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
    if args.rand:
        df = pd.read_csv(args.input, index_col=0) # read corr
        print('generating random graphs')
        _, stats = cor2g_rand(df, args.m, args.out, args.steps)
        stats.to_csv(f'{args.out}_stats.tsv', index=False, sep ='\t')
    else:
        df = pd.read_csv(args.input) # read rank
        print('constructing graphs')
        _, stats = rank2g(df, args.m, args.out, args.steps)
        stats.to_csv(f'{args.out}_stats.tsv', index=False, sep ='\t')
    print('done')
main()



