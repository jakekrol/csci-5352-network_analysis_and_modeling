#!/usr/bin/env python3

import sys
import os
import networkx as nx
import torch
import pandas as pd
import glob

### compute stats
# def get_dist_stats(x):
#     print('get_dist_stats')
#     m = -1
#     mu = -1
#     n_paths = 0
#     s_geo = 0
#     for k1,v1 in x.items():
#         for k2,v2 in v1.items():
#             m = max(m,v2)
#             n_paths += 1
#             s_geo += v2
#     mu = s_geo / n_paths
#     print("diameter",m)
#     print("average geodesic path length",mu)
#     print("number of paths",n_paths)
#     return m,mu, n_paths

# d = '/data/jake/csci-5352-network_analysis_and_modeling/ps1_apsp'
# files = os.listdir(d)
# do = '/data/jake/csci-5352-network_analysis_and_modeling/ps1_ec_distance_stats'
# print(files)
# c = ['file', 'l_max', 'l_mean', 'n_paths']
# df = pd.DataFrame(columns = c)
# for f in files:
#     print(f)
#     f = os.path.join(d,f)
#     x = torch.load(f)
#     m,mu,n_paths = get_dist_stats(x)
#     df = pd.concat([df, pd.DataFrame([[f,m,mu,n_paths]], columns=c)])
# df.to_csv(os.path.join(do,'distance_stats.tsv'),sep='\t', index=False)

### small example get diameter
# took about 2-3 minutes to run
# could parallelize over the outer loop
# and then reduce the results with max
# m = -1
# mu = -1
# n = 0
# s_distances = 0
# for k1,v1 in d.items():
#     for k2,v2 in v1.items():
#         print(v2)
#         m = max(m,v2)
#         n+=1
#         s_distances += v2
# print("diameter",m)

### compute n and largest component for each network
# d = '/data/jake/csci-5352-network_analysis_and_modeling/facebook100txt'
# files = glob.glob(d + '/*.txt')
# do = '/data/jake/csci-5352-network_analysis_and_modeling/ps1_ec_distance_stats'
# print(files)
# c = ['file', 'n', 'largest_component']
# df = pd.DataFrame(columns = c)
# for f in files:
#     G = nx.read_edgelist(f,nodetype=int)
#     n = G.number_of_nodes()
#     largest_component = len(max(nx.connected_components(G), key=len))
#     print(f,n,largest_component)
#     df = pd.concat([df, pd.DataFrame([[f,n,largest_component]], columns=c)])
# df.to_csv(os.path.join(do,'network_stats.tsv'),sep='\t', index=False)

# join the two tables by the  file column
df1 = pd.read_csv('/data/jake/csci-5352-network_analysis_and_modeling/ps1_ec_distance_stats/network_stats.tsv', sep='\t')
df2 = pd.read_csv('/data/jake/csci-5352-network_analysis_and_modeling/ps1_ec_distance_stats/distance_stats.tsv', sep='\t')
df1['file'] = df1['file'].apply(lambda x: os.path.basename(x).split('.')[0])
df1['file'] = df1['file'].apply(lambda x: x.replace(' ', '_'))
df2['file'] = df2['file'].apply(lambda x: os.path.basename(x).split('.')[0])
print(df1)
print(df2)
df = pd.merge(df2, df1, on='file')
print(df)

### plot l_max versus n
import matplotlib.pyplot as plt
plt.scatter(df['l_max'],df['n'])
plt.xlabel('Diameter ($l_{max}$)', fontsize=18)
plt.ylabel('Number of nodes ($n$)', fontsize=18)
plt.title('Diameter versus number of nodes in full graph')
plt.savefig('l_max_vs_n.png')
plt.close()

# plot average geodesic path length versus largest component size

plt.scatter(df['l_mean'],df['largest_component'])
plt.xlabel("Average geodesic path length ($E[l]$)", fontsize=18)
plt.ylabel('Size of largest component', fontsize=18)
plt.title('Average geodesic path length versus size of largest component')
plt.savefig('l_mean_vs_largest_component.png')

