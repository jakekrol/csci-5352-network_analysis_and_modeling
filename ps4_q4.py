#!/usr/bin/env python3
import copy
import math
import numpy as np
import networkx as nx
import sys
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 12})  # Change 14 to your desired font size

kappas=[10,10]
M_dc = np.array([[8,2],[2,8]])
def dcsbm_l(M,kappas):
    L = 0
    for r in range(M.shape[0]):
        for s in range(M.shape[1]):
            if M[r,s] > 0:
                L += M[r,s] * math.log(M[r,s] / (kappas[r] * kappas[s]))
    return L
# print(dcsbm_l(M_dc,kappas))

g = nx.Graph()
g.add_edge(1,2)
g.add_edge(1,3)
g.add_edge(1,6)
g.add_edge(1,7)
g.add_edge(1,8)
g.add_edge(1,9)
g.add_edge(3,4)
g.add_edge(3,6)
g.add_edge(4,6)
g.add_edge(5,6)

def g2M(g,z,c):
    '''
    graph to mixing matrix
    '''
    M = np.zeros((c,c))
    for i,j in g.edges():
        r = z[i-1]
        s = z[j-1]
        if r == s:
            M[r,s] += 2 # double count within group edges
        else:
            M[r,s] += 1
            M[s,r] += 1
    return M
# print(g2M(g,[0,0,1,1,1,1,0,0,0],2))

def makeAMove(g,z_t, c,f):
    '''
    g: graph
    z_t: node labels
    c: number of communities
    f: frozen vector
    return: (lstar, node, community)
    '''
    lstar = -1000000000
    # get unfrozen nodes
    unfrozen = []
    for i,fi in enumerate(f):
        if fi == 0:
            unfrozen.append(i+1)
    for vertex in unfrozen:
        c_i = z_t[vertex-1] # community of node i
        newcomm = set(z_t).difference({c_i})
        for j in newcomm:
            z_c = copy.deepcopy(z_t)
            # move node i to community j
            z_c[vertex-1] = j
            M = g2M(g,z_c,c) # mixing matrix
            kappas = np.sum(M,axis=1) # group degrees
            l = dcsbm_l(M,kappas)
            if l > lstar:
                lstar = l
                vstar = vertex
                z_i = j
            print('lstar:',lstar)
    return lstar, vstar, z_i


def plotg(g,t,file):
    color_map = []
    for node in g:
        if g.nodes[node]['label'] == 0:
            color_map.append('red')
        elif g.nodes[node]['label'] == 1:
            color_map.append('orange')
        else:
            color_map.append('blue')

    # Draw the graph
    plt.figure()
    plt.title(t)
    nx.draw(g, with_labels=True, node_color=color_map, edge_color='gray', node_size=500, font_size=10)

    # Show the plot
    plt.title(t)
    print(t)
    plt.savefig(file)
    plt.close()

def plot2g(g1,g2,t1,t2,file):
    color_map = []
    for node in g1:
        if g1.nodes[node]['label'] == 0:
            color_map.append('red')
        elif g1.nodes[node]['label'] == 1:
            color_map.append('orange')
        else:
            color_map.append('blue')
    fig, axs = plt.subplots(1,2)
    nx.draw(g1, with_labels=True, node_color=color_map, edge_color='gray', node_size=500, font_size=10,ax=axs[0])
    color_map = []
    for node in g2:
        if g2.nodes[node]['label'] == 0:
            color_map.append('red')
        elif g2.nodes[node]['label'] == 1:
            color_map.append('orange')
        else:
            color_map.append('blue')
    nx.draw(g2, with_labels=True, node_color=color_map, edge_color='gray', node_size=500, font_size=10,ax=axs[1])
    axs[0].set_title(t1)
    axs[1].set_title(t2)
    plt.savefig(file)
    plt.close()



# ### q4a
# # input graph
# c=3
# # np.random.seed(0)
# z = np.random.choice([0, 1, 2], size=9)
# for i,x in enumerate(z):
#     g.nodes[i+1]['label'] = x
# print(z)
# f = np.array([0,1,0,0,0,0,0,0,0])
# # plotg(g,'q4a.png')
# M_g = g2M(g,z,c)
# kappas = np.sum(M_g,axis=1)
# l_g = dcsbm_l(M_g,kappas)
# # output graph
# lstar, vstar,z_i = makeAMove(g,z,c,f)
# print('lstar:',lstar)
# print('vertex:',vstar)
# print('z_i:',z_i)
# g_c = g.copy()
# g_c.nodes[vstar]['label'] = z_i

# plot2g(g,g_c,f'Before move (Log(L)={round(l_g,2)})',f'After move (Log(L={round(lstar,2)}))','q4a.png')

def runOnePhase(g,z,c,f):
    '''
    g: graph
    z: node labels
    c: number of communities
    f: frozen vector
    return: (z, l)
    '''
    # compute original log likelihood
    z0=copy.deepcopy(z)
    M_g = g2M(g,z,c)
    kappas = np.sum(M_g,axis=1)
    l0 = dcsbm_l(M_g,kappas)
    lhoods=[]
    m_lstar = l0
    halt = 1 # stopping criteria for next phase
    while sum(f) < len(f): # while there are still unfrozen nodes
        lstar, vstar, z_i = makeAMove(g,z,c,f) # make a move
        # freeze the node
        f[vstar-1] = 1
        # update z
        z[vstar-1] = z_i
        lhoods.append(lstar)
        if lstar > m_lstar:
            m_lstar = lstar
            zstar = copy.deepcopy(z)
            halt = 0 # will have a next phase
    # get max log likelihood
    lstar = max(lhoods)
    if halt == 1:
        zstar = z0 # revert to original z
    lhoods.insert(0,l0)
    return zstar, lstar, halt , lhoods # best partition, best log likelihood, stopping criteria, log likelihoods

        

### q4b
# # input graph
# c=3
# # np.random.seed(0)
# z = np.random.choice([0, 1, 2], size=9)
# for i,x in enumerate(z):
#     g.nodes[i+1]['label'] = x
# print(z)
# f = np.array([0,0,0,0,0,0,0,0,0])
# M1 = g2M(g,z,c)
# kappas1 = np.sum(M1,axis=1)
# l1 = dcsbm_l(M1,kappas1)
# # output graph
# zstar, lstar, halt, lhoods = runOnePhase(g,z,c,f)
# print('zstar:',zstar, 'lstar:',lstar, 'halt:',halt)
# print('lhoods:',lhoods)
# g2 = g.copy()
# for i,x in enumerate(zstar):
#     g2.nodes[i+1]['label'] = x
# plot2g(g,g2,f'Before move (Log(L)={round(l1,2)})',f'After move (Log(L={round(lstar,2)}))','q4b_g.png')
# # plot the likelihoods
# plt.plot(list(range(len(lhoods))), lhoods)
# plt.xlabel('Number of moves')
# plt.ylabel('Log likelihood')
# plt.savefig('q4b_l.png')
# plt.close()

def fitDCSBM(g,c,z,T):
    # initial log likelihood
    M = g2M(g,z,c)
    kappas = np.sum(M,axis=1)
    lstar = dcsbm_l(M,kappas)
    zstar = copy.deepcopy(z)
    pi = 0
    lhoods = []
    for p in range(T):
        f = np.zeros(len(z))
        z_p,l_p,halt,lhoods_p = runOnePhase(g,zstar,c,f)
        if l_p > lstar:
            lstar = l_p
            zstar = copy.deepcopy(z_p)
        lhoods += lhoods_p
        pi +=1
        if halt == 1:
            break
    pc = pi * (len(z)+1)
    
    return zstar,lstar,pc,lhoods


### q4c
# # input graph
# g = nx.Graph()
# g.add_edge(1,2)
# g.add_edge(1,3)
# g.add_edge(1,6)
# g.add_edge(1,7)
# g.add_edge(1,8)
# g.add_edge(1,9)
# g.add_edge(3,4)
# g.add_edge(3,6)
# g.add_edge(4,6)
# g.add_edge(5,6)
# z = np.random.choice([0, 1, 2], size=9)
# c = 3
# T = 30
# zstar,lstar,pc,lhoods = fitDCSBM(g,c,z,T)
# print('zstar:',zstar, 'lstar:',lstar, 'pc:',pc)
# g2 = g.copy()
# for i,x in enumerate(zstar):
#     g2.nodes[i+1]['label'] = x
# plotg(g2,f'Final partition (Log(L)={round(lstar,2)})','q4c.png')
# # plot the likelihoods
# plt.plot(list(range(len(lhoods))), lhoods)
# plt.xlabel('Number of moves')
# plt.ylabel('Log likelihood')
# plt.savefig('q4c_l.png')
# plt.close()

# # report final M and kappas
# M = g2M(g2,zstar,c)
# kappas = np.sum(M,axis=1)
# print('Final M and kappas:')
# print('M:',M)
# print('kappas:',kappas)

### q4d
# input graph
g = nx.read_gml('karate.gml', label=None)
f = np.zeros(len(g.nodes()))
z = np.random.choice([0, 1], size=len(g.nodes()))
T=30
c=2
zstar,lstar,pc,lhoods = fitDCSBM(g,c,z,T)
print('zstar:',zstar, 'lstar:',lstar, 'pc:',pc)
for i,x in enumerate(zstar):
    g.nodes[i+1]['label'] = x
plotg(g,f'Final partition (Log(L)={round(lstar,2)})','q4d.png')
# plot the likelihoods
plt.plot(list(range(len(lhoods))), lhoods)
plt.xlabel('Number of moves')
plt.ylabel('Log likelihood')
plt.savefig('q4d_l.png')

M = g2M(g,zstar,c)
kappas = np.sum(M,axis=1)
print('Final M and kappas:')
print('M:',M)
print('kappas:',kappas)











