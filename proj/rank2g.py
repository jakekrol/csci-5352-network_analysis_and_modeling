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
k = int(args[1])

df = pd.read_csv(input)
print(df)
g = nx.Graph()
for i,row in df.iterrows():
    sym1 = row['sym1']
    sym2 = row['sym2']
    cor = row['cor']
    print(sym1,sym2,cor)
    g.add_edge(sym1,sym2, weight = cor)
    if i == k-1:
        break
print(g)
# plot graph
net = Network(notebook=False)
net.from_nx(g)
net.write_html('g.html')