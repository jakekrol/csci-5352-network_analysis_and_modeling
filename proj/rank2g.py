#!/usr/bin/env python3
# input rank file
# output graph

import os,sys
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pyvis.network import Network


args = sys.argv[1:]
input = args[0]
m = int(args[1])

df = pd.read_csv(input)
print(df)
g = nx.Graph()
ms = []
mean_degs = []
Cs = []
n_lccs = []
diameters = []
for i,row in df.iterrows():
    sym1 = row['sym1']
    sym2 = row['sym2']
    cor = row['cor']
    print(sym1,sym2,cor)
    g.add_edge(sym1,sym2, weight = cor)
    if i == m-1:
        break
    # compute statistics
    mean_deg = sum(dict(g.degree()).values()) / g.number_of_nodes()
    C = nx.transitivity(g)
    lcc = max(nx.connected_components(g), key=len)
    n_lcc = len(lcc)
    # diameter w.r.t largest connected component
    if n_lcc > 1:
        diameter = nx.diameter(g.subgraph(lcc))
    else:
        diameter = 0
    ms.append(i+1)
    mean_degs.append(mean_deg)
    Cs.append(C)
    n_lccs.append(n_lcc)
    diameters.append(diameter)
print(g)
# plot graph
net = Network(notebook=False)
net.from_nx(g)
net.write_html('g.html')

pd.DataFrame({'m':ms,'mean_deg':mean_degs,'C':Cs,'n_lcc':n_lccs,'diameter':diameters}).to_csv('stats.csv',index=False)  