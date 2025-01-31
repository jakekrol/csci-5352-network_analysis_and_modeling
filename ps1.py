#!/usr/bin/env python3


# first clean out attribute files
# ls | grep "attr" | gargs_linux -p 1 -o "mv {0} attr"
# mv a few more with spaces in names
import networkx as nx
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import torch
import plotly.express as px
import plotly.graph_objects as go
import sys

din='/home/jake/ghub/csci-5352-network_analysis_and_modeling/facebook100txt'

FONTSIZE=18

###
# Q5a
# print("Q5a")

### compute k avg
# files = glob.glob(din + '/*.txt')

# def k_avg(f):
#     G = nx.read_edgelist(f,nodetype=int)
#     k_tot = sum(dict(G.degree()).values())
#     n = G.number_of_nodes()
#     k_avg = k_tot / n
#     return k_avg

# d_k = {}

# for i,f in enumerate(files):
#     k = k_avg(f)
#     name = os.path.basename(f).split('.')[0]
#     # rm spaces
#     name = name.replace(' ', '_')
#     d_k[name] = k
#     print(i, name, k)
# print(d_k)
# pd.DataFrame(d_k.items(), columns=['name', 'k_avg']).to_csv('k_avg.tsv', index=False, sep = '\t')

### plot histogram
# df = pd.read_csv('k_avg.tsv', sep = '\t')
# df.hist(column='k_avg', bins=30)
# plt.xlabel('Average degree', fontsize=FONTSIZE)
# # make ylabel with fontsize
# plt.ylabel('Count', fontsize=FONTSIZE)
# plt.grid(False)
# plt.title('Average degree of Facebook networks', fontsize=FONTSIZE)

# plt.savefig('k_avg_hist.png')

# print("End Q5a")
###

###
# Q5c
# print("Q5c")
### COMPUTE
# compute avg nb degree and node degree
# files = glob.glob(din + '/*.txt')

# def mean_neighbor_degree(G):
#     n = G.number_of_nodes()
#     k_sq = sum([d**2 for n,d in G.degree()]) / n
#     k = sum(dict(G.degree()).values()) / n
#     k_nb = k_sq/k
#     return k, k_nb

# d_k={}
# for i,f in enumerate(files):
#     G= nx.read_edgelist(f, nodetype=int)
#     k_avg, k_nb = mean_neighbor_degree(G)
#     name = os.path.basename(f).split('.')[0]
#     # rm spaces
#     name = name.replace(' ', '_')
#     d_k[name] = [k_avg, k_nb]
#     print(i, name, k_avg, k_nb)
# print(d_k)
# torch.save(d_k, 'k_nb.pt')

### LOAD AND PLOT
# d = torch.load('k_nb.pt')
# df = pd.DataFrame(d).T
# df.columns = ['k_avg', 'k_nb']
# df['ratio'] = df['k_nb'] / df['k_avg']
# print(df)

# # plot k_avg vs k_nb
# # x axis is k_avg
# # y axis is k_nb
# fig = px.scatter(df, x='k_avg', y='ratio')
# fig.update_layout(
#     title='Neighbor paradox',
#     xaxis_title='Mean degree',
#     yaxis_title='Ratio of mean neighbor degree to mean degree',
#     font=dict(
#         size=FONTSIZE - 3
#     )
# )
# xmax = df['k_avg'].max()
# ymax = df['ratio'].max()
# # draw dotted line at y=1
# fig.add_shape(
#     type='line',
#     x0=0,
#     y0=1,
#     x1=xmax + 10,
#     y1=1,
#     line=dict(
#         color='black',
#         width=1,
#         dash='dash'
#     ),
#     # add legend for line
#     name='No paradox line'
# )
# # plain background yet keep the axes lines
# fig.update_layout(
#     plot_bgcolor="white",  # Minimal background color
#     xaxis=dict(
#         showline=True,  # Show x-axis line
#         linewidth=2,
#         linecolor="black",  # Line color
#         showgrid=False,  # Remove gridlines
#     ),
#     yaxis=dict(
#         showline=True,  # Show y-axis line
#         linewidth=2,
#         linecolor="black",  # Line color
#         showgrid=False,  # Remove gridlines
#     )
# )
# # add legend for dashed line
# fig.update_layout(legend=dict(
#     yanchor="top",
#     y=0.5,
#     xanchor="left",
#     x=0.80
# ))

# fig.add_trace(go.Scatter(
#     x=[None],  # No actual points, just for the legend
#     y=[None],
#     mode="lines",
#     line=dict(color="black", dash="dash"),
#     name="No paradox",  # Label for the legend
# ))

# # annotate the nodes for the following colleges
# annotations = ["Reed98", "Colgate88", "Mississippi66", "Virginia63", "Berkeley13"]
# for i, name in enumerate(annotations):
#     fig.add_annotation(
#         x=df.loc[name, 'k_avg'],
#         y=df.loc[name, 'ratio'],
#         text=name,
#         showarrow=True,
#         arrowhead=2,
#         font=dict(
#             size=12,
#             color="dark orange"
#         ),
#         # have arrow point from the right
#         ax=25,
#         ay=-20
#     )


# # set x and y max to be the same, 250
# fig.update_yaxes(range=[0, ymax])
# fig.write_image('k_avg_vs_k_nb.png')

### Q5c end

### Q5e
print("Q5e")
files = glob.glob(din + '/*.txt')
dout = '/home/jake/ghub/csci-5352-network_analysis_and_modeling/ps1_apsp'
# G = nx.read_edgelist(files[0], nodetype=int)
def g_lc(G):
    largest_cc = max(nx.connected_components(G), key=len)
    G = G.subgraph(largest_cc).copy()
    return G
# print("Number of nodes", G.number_of_nodes())
# G_lc = g_lc(G)
# print("Number of nodes in largest connected component", G_lc.number_of_nodes())

# compute all pairs shortest paths in LC
# apsp = dict(nx.all_pairs_shortest_path_length(G_lc))
# torch.save(apsp, 'apsp.pt')

for i,f in enumerate(files):
    G = nx.read_edgelist(f,nodetype=int)
    G_lc = g_lc(G)
    apsp = dict(nx.all_pairs_shortest_path_length(G_lc))
    name = os.path.basename(f).split('.')[0]
    name = name.replace(' ', '_')
    out = os.path.join(dout, name + '.pt')
    torch.save(apsp, out)
    print(i, name, out)
print("End Q5e")