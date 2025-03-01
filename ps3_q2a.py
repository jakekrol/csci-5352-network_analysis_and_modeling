#!/usr/bin/env python3
import networkx as nx
import math
import numpy as np
import random
from sklearn.metrics import auc
from sklearn.metrics import roc_curve
import pandas as pd
import itertools
import os,sys
import warnings
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt

# Ignore FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

### example graph
G =nx.Graph()
G.add_edges_from([(0,3),(1,3),(2,3),(2,7),(3,4),(4,5),(4,6),(4,7)])
G.add_node(8)

### score functions
def random_noise():
    return random.uniform(0.00000001,0.00000002)

def jc(G,i,j):
    nb_i = set(G.neighbors(i))
    nb_j = set(G.neighbors(j))
    i = nb_i.intersection(nb_j)
    u = nb_i.union(nb_j)
    if len(u) == 0:
        return 0 + random_noise()
    else:
        return len(i)/len(u) + random_noise()

def dp(G,i,j):
    k_i = G.degree(i)
    k_j = G.degree(j)
    return k_i*k_j + random_noise()
def SP(G,i,j):
    try:
        return 1/nx.shortest_path_length(G,i,j) + random_noise()
    except nx.NetworkXNoPath:
        return 0 + random_noise()
    

### test score functions
# print("JC")
# print(jc(G,0,1))
# print(jc(G,3,4))
# print(jc(G,2,4))
# print(jc(G,0,8))
# print("DP")
# print(dp(G,0,1))
# print(dp(G,3,4))
# print(dp(G,2,4))
# print(dp(G,0,8))
# print("SP")
# print(SP(G,0,1))
# print(SP(G,3,4))
# print(SP(G,2,4))
# print(SP(G,0,8))

def score_tbl():
    d = pd.DataFrame({
        'i': [1,2,3,4],
        'j': [2,3,4,5],
        # 'tao': [1,1,0,0], # auc 1.0
        'tao': [0,1,0,0], # auc 0.66
        'score': [1,0.75,0.5,0.25]
    })
    return d

### AUC
# def auc(tbl, key):
#     tbl_c = tbl.copy()
#     tbl_c = tbl_c.sort_values(by=key,ascending=False).reset_index(drop=True)
#     n = len(tbl_c)
#     P = tbl_c[tbl_c['tao'] == 1].shape[0]
#     N = tbl_c[tbl_c['tao'] == 0].shape[0]
#     # add prediction column
#     tbl_c['pred'] = 0
#     # important that index is reset after sorting
#     print('computing auc')
#     tprs=[]
#     fprs=[]
#     for i in range(n):
#         if N == 0:
#             fprs.append(0)
#             continue
#         if P == 0:
#             tprs.append(0)
#             continue
#         # get tps, only need to search upto threshold since everything below
#         # is predicted negative
#         # also precomputing P and N, is efficient
#         tp = 0
#         for j in range(0,i+1):
#             if tbl_c.loc[j,'tao'] == 1:
#                 tp += 1
#         tprs.append(tp/P)
#         # get fps
#         fp = 0
#         for j in range(0,i+1):
#             if tbl_c.loc[j,'tao'] == 0:
#                 fp += 1
#         fprs.append(fp/N)
#         print(f'{i}/{n-1}')
        
#     # tbl_c['tpr'] = tprs
#     # tbl_c['fpr'] = fprs
#     # for i,_ in enumerate(tprs):
#     #     if tprs[i] < 0:
#     #         raise ValueError('tpr < 0')
#     # for i,_ in enumerate(fprs):
#     #     if tprs[i] < 0:
#     #         raise ValueError('fpr < 0')
#     auc = np.trapz(tprs,fprs)
#     return tprs, fprs, auc

def auc2(scores, truth):
    auc = roc_auc_score(truth, scores)
    return auc

### test auc
# print(score_tbl())
# tbl, stat = auc(score_tbl())
# print(tbl)
# print(stat)

def mask_edges(G,f):
    G_m = G.copy()
    m = G.number_of_edges()
    # setup fraction
    if f < 0.5:
        # sample m * f edges & mask the rest
        s = math.floor(m * f)
        action = 'keep'
    else:
        # sample m - (m*f) edges & mask them
        s = math.floor(m * (1-f))
        action = 'mask'
    # sample
    E = set(G.edges())
    sample_edges = set()
    for s_i in range(s):
        edge = random.choice(list(E))
        E.remove(edge)
        sample_edges.add(edge)
    # assign masked edges
    masked_edges = set()
    if action == 'keep':
        masked_edges = set(E) - sample_edges
    else:
        masked_edges = sample_edges
    for E_i in masked_edges:
        G_m.remove_edge(*E_i)
    return G_m, masked_edges

### test mask_edges
# print('Test mask_edges')
# print('Original graph')
# print(G.edges())    
# print('Masked graph')
# G_m, masked_edges = mask_edges(G,0.5)
# print(G_m.edges())
# print('Masked edges')
# print(masked_edges)

f_i = 0.05
F=[f_i]
while f_i < 0.95:
    f_i += 0.05
    f_i = round(f_i,2)
    F.append(f_i)
def experiment(G,F=F,k=50):
    # fraction observed edges
    aucs_jc = []
    aucs_dp = []
    aucs_sp = []
    for f in F:
        auc_jc = 0
        auc_dp = 0
        auc_sp = 0
        # repititions
        for i in range(k):
            # mask
            G_m, masked_edges = mask_edges(G,f)
            # possible edges
            X = set(itertools.combinations(G_m.nodes(),2))
            X = X - set(G_m.edges())
            # score edges
            ies=[]
            js=[]
            taos=[]
            score_jcs=[]
            score_dps=[]
            score_sps=[]
            # mp = len(X)
            for idx,e in enumerate(X):
                i = e[0]
                j = e[1]
                # truth
                if (i,j) in masked_edges:
                    tao = 1
                else:
                    tao = 0
                score_jc = jc(G_m,i,j)
                score_dp = dp(G_m,i,j)
                score_sp = SP(G_m,i,j)
                ies.append(i)
                js.append(j)
                taos.append(tao)
                score_jcs.append(score_jc)
                score_dps.append(score_dp)
                score_sps.append(score_sp)
            # compute auc for each clasiifier
            # jc
            stat = auc2(score_jcs, taos)
            auc_jc += stat
            # dp
            stat = auc2(score_dps, taos)
            auc_dp += stat
            # sp
            stat = auc2(score_sps, taos)
            auc_sp += stat
        # average auc
        print("f_i: ", f)
        print("auc_jc: ", auc_jc/k)
        print("auc_dp: ", auc_dp/k)
        print("auc_sp: ", auc_sp/k)
        aucs_jc.append(auc_jc/k)
        aucs_dp.append(auc_dp/k)
        aucs_sp.append(auc_sp/k)
    return aucs_jc, aucs_dp, aucs_sp
    

# experiment


### test experimnet/auc
# aucs_jc, aucs_dp, aucs_sp = experiment(G,F=F,k=50)
# df = pd.DataFrame({
#     'f': F,
#     'auc_jc': aucs_jc,
#     'auc_dp': aucs_dp,
#     'auc_sp': aucs_sp
# })
# df.to_csv('ps3_aucs.tsv',sep='\t',index=False)

# G_m, masked_edges = mask_edges(G,0.5)
# # edges to predict
# X = set(itertools.combinations(G_m.nodes(),2))
# X = X - set(G_m.edges())
# # score edges
# df_score = pd.DataFrame(
#     columns=['i','j','tao','score_jc',
#             'score_dp','score_sp']
# )
# for idx,e in enumerate(X):
#     i = e[0]
#     j = e[1]
#     # truth
#     if (i,j) in masked_edges:
#         tao = 1
#     else:
#         tao = 0
#     score_jc = jc(G_m,i,j)
#     score_dp = dp(G_m,i,j)
#     score_sp = SP(G_m,i,j)
#     df_score = pd.concat(
#         [df_score,
#             pd.DataFrame({
#             'i': [i],
#             'j': [j],
#             'tao': [tao],
#             'score_jc': [score_jc],
#             'score_dp': [score_dp],
#             'score_sp': [score_sp]
#             },index=[idx])
#         ]
#     )
# print(df_score)
# # compute auc for each clasiifier
# # jc
# tpr, fpr,auc = auc(df_score,'score_jc')
# print("JC") 
# print(tpr, fpr, auc)
# print(df_score[['i','j','tao','score_jc']].sort_values('score_jc',ascending=False).reset_index(drop=True))

### net1m
# G = nx.read_edgelist('net1m_edges.csv',delimiter=',',data=False,nodetype=int)
# # experiment
# aucs_jc, aucs_dp, aucs_sp = experiment(G,F=F,k=5)
# df = pd.DataFrame({
#     'f': F,
#     'auc_jc': aucs_jc,
#     'auc_dp': aucs_dp,
#     'auc_sp': aucs_sp
# })
# df.to_csv('net1m_aucs.tsv',sep='\t',index=False)

### hvr
# G = nx.read_edgelist('HVR_5.txt',delimiter=',',data=False,nodetype=int)
# # experiment
# aucs_jc, aucs_dp, aucs_sp = experiment(G,F=F,k=5)
# df = pd.DataFrame({
#     'f': F,
#     'auc_jc': aucs_jc,
#     'auc_dp': aucs_dp,
#     'auc_sp': aucs_sp
# })
# df.to_csv('hvr5_aucs.tsv',sep='\t',index=False)

### plot AUCs
fig, (ax1,ax2) = plt.subplots(1,2)
df_n = pd.read_csv('net1m_aucs.tsv', delimiter='\t')
df_h = pd.read_csv('hvr5_aucs.tsv', delimiter='\t')
ax1.plot(df_n['f'], df_n['auc_jc'], label='JC')
ax1.plot(df_n['f'], df_n['auc_dp'], label='DP')
ax1.plot(df_n['f'], df_n['auc_sp'], label='SP')
ax1.set_xlabel('f (fraction of edges observed)')
ax1.set_ylabel('AUC')
ax1.set_title('net1m')
ax1.set_ylim(0.4,1)
ax1.plot([0,1], [0.5,0.5], linestyle='--', color='black', label = 'AUC=0.5')
ax1.legend()
ax2.plot(df_h['f'], df_h['auc_jc'], label='JC')
ax2.plot(df_h['f'], df_h['auc_dp'], label='DP')
ax2.plot(df_h['f'], df_h['auc_sp'], label='SP')
ax2.set_xlabel('f (fraction of edges observed)')
ax2.set_title('hvr5')
ax2.set_ylim(0.4,1)
ax2.plot([0,1], [0.5,0.5], linestyle='--', color='black', label = 'AUC=0.5')
ax2.legend()
plt.savefig('ps3_q2a.png')

def experiment2(G,f=0.8):
    # mask
    G_m, masked_edges = mask_edges(G,f)
    # possible edges
    X = set(itertools.combinations(G_m.nodes(),2))
    X = X - set(G_m.edges())
    # score edges
    ies=[]
    js=[]
    taos=[]
    score_jcs=[]
    score_dps=[]
    score_sps=[]
    # mp = len(X)
    for idx,e in enumerate(X):
        i = e[0]
        j = e[1]
        # truth
        if (i,j) in masked_edges:
            tao = 1
        else:
            tao = 0
        score_jc = jc(G_m,i,j)
        score_dp = dp(G_m,i,j)
        score_sp = SP(G_m,i,j)
        ies.append(i)
        js.append(j)
        taos.append(tao)
        score_jcs.append(score_jc)
        score_dps.append(score_dp)
        score_sps.append(score_sp)
    # compute auc for each clasiifier
    # jc
    # print('scores')
    # print(score_jcs)
    # print('taos')
    # print(taos)
    
    fpr_jc,tpr_jc,_ = roc_curve(taos, score_jcs)
    auc_jc = auc(fpr_jc,tpr_jc)
    # dp
    fpr_dp,tpr_dp,_ = roc_curve(taos, score_dps)
    auc_dp = auc(fpr_dp,tpr_dp)
    # sp
    fpr_sp,tpr_sp,_ = roc_curve(taos, score_sps)
    auc_sp = auc(fpr_sp,tpr_sp)
    return {'jc': [fpr_jc,tpr_jc,auc_jc],'dp': [fpr_dp,tpr_dp,auc_dp],'sp': [fpr_sp,tpr_sp,auc_sp]}

### experiment 2
# read hvr graph
G = nx.read_edgelist('HVR_5.txt',delimiter=',',data=False,nodetype=int)
d = experiment2(G,f=0.8)
# plot
fig = plt.figure()
plt.plot(d['jc'][0],d['jc'][1],label='JC')
plt.plot(d['dp'][0],d['dp'][1],label='DP')
plt.plot(d['sp'][0],d['sp'][1],label='SP')
plt.plot([0,1],[0,1],linestyle='--',color='black')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC of JC, DP, SP link predictors for HVR network')
plt.legend()
plt.savefig('ps3_q2a_roc.png')



