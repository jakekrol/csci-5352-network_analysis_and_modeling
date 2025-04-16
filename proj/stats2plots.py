#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import numpy as np


# for experiment 1
# input: stats file
# output: plot of stats

parser = argparse.ArgumentParser(description='Stats to Plot')
parser.add_argument('--input', '-i', type=str, required=True, help='input stats file')
parser.add_argument('--output', '-o', type=str, required=True, help='output plot file')
# parser.add_argument('--title', '-t', type=str, required=True, help='plot title')
# parser.add_argument('--xlabel', '-x', type=str, required=True, help='x-axis label')
# parser.add_argument('--ylabel', '-y', type=str, required=True, help='y-axis label')
# parser.add_argument('--stats', '-s', type=str, required=True, help='comma delim stats to plot')
parser.add_argument('--stats', '-s', type=int, required=True, help='1 for C,modularity and 2 for all other stats')
parser.add_argument('--tick_size', '-ts', type=int, default=10, help='tick size')
parser.add_argument('--legend_size', '-ls', type=int, default=10, help='legend size')

args = parser.parse_args()

# STATS = set(['mean_deg', 'C', 'n_lcc', 'diameter', 'n_comp', 'modularity'])
# stats = set(args.stats.split(','))
# assert stats.issubset(STATS), f"Invalid stats: {stats - STATS}. Valid stats are: {STATS}"

# read stats file
df = pd.read_csv(args.input, sep='\t')

# plot all stats as a function of 'm' column

# for s in stats:
#     if s == 'n_lcc':
#         df[s] = df[s].apply(lambda x: np.log2(x) if x > 0 else 0)
#     plt.plot(df['m'], df[s], label=s)
if args.stats == 1:
    # plot C and modularity
    plt.plot(df['m'], df['C'], label='clustering coef. (C)')
    plt.plot(df['m'], df['modularity'], label='modularity')
    plt.hlines(y=0,xmin=0,xmax=1000, color='black', linestyle='dashed', label = 'not (dis)assortative', alpha=0.3)
    plt.ylim(-1, 1)
elif args.stats == 2:
    # plot all other stats
    plt.plot(df['m'], df['mean_deg'], label='mean degree (<k>)')
    plt.plot(df['m'], df['n_lcc'].apply(lambda x: np.log2(x)), label='log2(|LCC|)')
    plt.plot(df['m'], df['diameter'], label='diameter (l_max)')
    plt.plot(df['m'], df['n_comp'].apply(lambda x: np.log2(x)), label='log2(num. components)')
    plt.ylim(0,40)
plt.xlabel('Number of edges (m)', fontsize=15)
if args.legend_size:
    plt.legend(fontsize=args.legend_size, framealpha=0.3)
else:
    plt.legend(framealpha=0.3)
if args.tick_size:
    plt.xticks(fontsize=args.tick_size)
    plt.yticks(fontsize=args.tick_size)
plt.savefig(args.output)
plt.close()


    # # C
    # plt.plot(df['m'], df['C'], label='C')
    # # n_lcc
    # plt.plot(df['m'], df['n_lcc'].apply(lambda x: np.log2(x)), label='log2(n_lcc)')
    # # diameter
    # plt.plot(df['m'], df['diameter'], label='diameter')
