#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import numpy as np


# input: stats file
# output: plot of stats

parser = argparse.ArgumentParser(description='Stats to Plot')
parser.add_argument('--input', '-i', type=str, required=True, help='input stats file')
parser.add_argument('--output', '-o', type=str, required=True, help='output plot file')
# parser.add_argument('--title', '-t', type=str, required=True, help='plot title')
# parser.add_argument('--xlabel', '-x', type=str, required=True, help='x-axis label')
# parser.add_argument('--ylabel', '-y', type=str, required=True, help='y-axis label')

args = parser.parse_args()

# read stats file
df = pd.read_csv(args.input, sep='\t')

# plot all stats as a function of 'm' column

# mean_deg
plt.plot(df['m'], df['mean_deg'], label='mean_deg')
# C
plt.plot(df['m'], df['C'], label='C')
# n_lcc
plt.plot(df['m'], df['n_lcc'].apply(lambda x: np.log10(x)), label='log10(n_lcc)')
# diameter
plt.plot(df['m'], df['diameter'], label='diameter')
plt.legend()
plt.savefig(args.output)
plt.close()


