#!/usr/bin/env python3

from collections import Counter
import networkx as nx
import statistics
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import random
import sys

### neighbor example
# G = nx.Graph()
# for i in range(8):
#     G.add_node(i, x=random.choice([1,2]))
# G.add_edge(0,3)
# G.add_edge(1,3)
# G.add_edge(2,3)
# G.add_edge(3,4)
# G.add_edge(4,5)
# G.add_edge(4,6)
# G.add_edge(4,7)

# colormap = []
# for node in G.nodes():
#     if G.nodes[node]['x'] == 1:
#         colormap.append('red')
#     else:
#         colormap.append('lightblue')
# fig, (ax1,ax2,ax3) = plt.subplots(1,3)
# # # plot
# nx.draw(G, with_labels=True,node_color=colormap,ax=ax1)
# ax1.set_title('Original graph')
# plt.savefig('g1.png')

# # neighbors
# print("Neighbors of node 4: ", list(G.neighbors(4)))
# print("Neighbors of node 3: ", list(G.neighbors(3)))
# print("Neighbors of node 0: ", list(G.neighbors(0)))

### norwegian graph
# G = nx.read_edgelist('net1m_edges.csv', delimiter=',', nodetype=int)
# df = pd.read_csv('net1m_nodes.csv', delimiter=',')
# print(df.head())

# # seems like 1 is male and 2 is female
# x_min = 10 ** 9
# x_max = -10 ** 9
# for i,row in df.iterrows():
#     n_i = row['index']
#     g_i = row['gender']
#     G.nodes[n_i]['gender'] = g_i
#     x_min = min(x_min, g_i)
#     x_max = max(x_max, g_i)
# print(G)
# print('Gender range: ', x_min, x_max) 
# a_i = 0
# alpha = [a_i]
# while a_i < 1:
#     a_i += 0.02
#     a_i = round(a_i, 2)
#     alpha.append(a_i)
# # print(alpha)


### functions
def mask_node_attrs(G, alpha, attr_key):
    G_c = G.copy()
    # assume attr is integer
    n = G_c.number_of_nodes()
    # number of nodes to sample
    if alpha < 0.5:
        # sample n * a_i nodes & mask the rest
        s = math.floor(n * alpha)
        action = 'keep'
    else:
        # sample n - (n*a_i) nodes & mask them
        s = math.floor(n * (1-alpha))
        action = 'mask'
    # sample
    nodes = set(range(n))
    sample_nodes = set()
    for s_i in range(s):
        node = random.choice(list(nodes))
        nodes.remove(node)
        sample_nodes.add(node)
    # assign masked nodes
    masked_nodes = set()
    if action == 'keep':
        masked_nodes = set(nodes) - sample_nodes
    else:
        masked_nodes = sample_nodes
    for node in masked_nodes:
        G_c.nodes[node][attr_key] = -1
        # G.nodes[node][attr_key] = random.choice(range(attr_min, attr_max+1))
    # get node data for masked nodes
    return G_c, masked_nodes

def mode(x):
    # compute modes and return set of any ties
    c = Counter(x)
    c = dict(c)
    s=set()
    m = -1 # count cannot be negative
    for k,val in c.items():
        if val > m:
            m = val
            s = {k}
        if val == m:
            s.add(k)
    return s
    

def local_smooth(G, masked_nodes, attr_key, attr_min, attr_max):
    G_c  = G.copy()
    # used to check if all neighbors are masked
    def is_nb_masked(x):
        if x == -1:
            True
        else:
            False
    # smooth masked nodes
    for node in masked_nodes:
        neighbors = set(list(G_c.neighbors(node)))
        # make sure to exclude neighboring masked nodes from smoothing
        # masked node set is constant throughout loop, so smoothing is not dependent on order
        neighbors = neighbors - masked_nodes
        # get neighbor attrs
        neighbor_attrs = []
        for neighbor in neighbors:
            neighbor_attrs.append(G_c.nodes[neighbor][attr_key])
        m = map(is_nb_masked, neighbor_attrs)
        # baseline 
        if all(m):
            G_c.nodes[node][attr_key] = random.choice(range(attr_min, attr_max+1))
            continue
        # drop masked neighbors
        neighbor_attrs = [x for x in neighbor_attrs if x != -1]
        # mode assuming categorical
        modes = mode(neighbor_attrs)
        if len(modes) == 1:
            G_c.nodes[node][attr_key] = modes.pop()
        else:
            # break ties at random
            G_c.nodes[node][attr_key] = random.choice(list(modes))
    return G_c


a_i = 0
ALPHAS = [a_i]
while a_i < 1:
    a_i += 0.02
    a_i = round(a_i, 2)
    ALPHAS.append(a_i)
def experiment(G,attr_key, alphas=ALPHAS,k=100):
    avas=[]
    n_alphas = len(alphas)
    print('Total alphas: ', n_alphas)
    for a_i in alphas:
        ava=0
        print('a_i: ', a_i)
        for k_i in range(k):
            # print('k_i: ', k_i)
            # mask nodes
            G_m, m_nodes = mask_node_attrs(G, alpha = a_i, attr_key=attr_key)
            # get original data of masked nodes
            G_sub = G.copy()
            G_sub = G_sub.subgraph(m_nodes)
            # smooth the masked nodes
            G_smooth = local_smooth(G_m, m_nodes, attr_key, 1, 2)
            # compute accuracy
            n = len(m_nodes)
            # if number of masked nodes is 0, then accuracy is 1
            if n == 0:
                ava += 1
                continue
            acc=0
            for node in m_nodes:
                if G_sub.nodes[node][attr_key] == G_smooth.nodes[node][attr_key]:
                    acc += 1
            acc = acc/n
            ava += acc
        ava = round(ava/k,2)
        avas.append(ava)
    return list(zip(alphas, avas))

### test code w/ neighbor example graph
# G, m_nodes = mask_node_attrs(G, alpha = 0.75, attr_key='x')
# print(m_nodes)
# colormap = []
# for node in G.nodes():
#     if G.nodes[node]['x'] == 1:
#         colormap.append('salmon')
#     elif G.nodes[node]['x'] == -1:
#         colormap.append('gray')
#     else:
#         colormap.append('skyblue')

# nx.draw(G, with_labels=True,node_color=colormap, ax=ax2)
# ax2.set_title('Masked graph')

# G = local_smooth(G, m_nodes, 'x', 1, 2)
# colormap = []
# for node in G.nodes():
#     if G.nodes[node]['x'] == 1:
#         colormap.append('red')
#     elif G.nodes[node]['x'] == -1:
#         colormap.append('gray')
#     else:
#         colormap.append('lightblue')
# nx.draw(G, with_labels=True,node_color=colormap, ax=ax3)
# ax3.set_title('Smoothed graph')
# plt.savefig('g.png')

# l = experiment(G)
# print(l)

### net1m
### experiment
# nodes.csv col 4 is gender attribute
# G = nx.read_edgelist('net1m_edges.csv',delimiter=',',data=False,nodetype=int)
# print(G)
# s = pd.read_csv('net1m_nodes.csv', delimiter=',', usecols=[3],comment='#',header=None).squeeze()
# print(type(s))
# print(s.head())
# for i in s.index:
#     G.nodes[i]['gender'] = s[i]
# l = experiment(G, attr_key='gender')
# pd.DataFrame(l, columns=['alpha', 'avg_acc']).to_csv('net1m_results.tsv', index=False,sep='\t')
# print(l)
### plot
# df_p = pd.read_csv('net1m_results.tsv', delimiter='\t')
# plt.plot(df_p['alpha'], df_p['avg_acc'])
# plt.xlabel('alpha (fraction of nodes observed)')
# plt.ylabel('average accuracy')
# plt.title('net1m average accuracy of local smoothing')
# plt.savefig('net1m_plot.png')

### hvr5
G = nx.read_edgelist('HVR_5.txt',delimiter=',',data=False,nodetype=int)
print(G)


    
        

            



    
        
        

            