#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

# input: correlation matrix
# output: histogram of correlations, mean, stddev

parser = argparse.ArgumentParser(description='Correlation to Histogram')
parser.add_argument('--input', '-i', type=str, required=True, help='input correlation matrix file')
parser.add_argument('--output', '-o', type=str, required=True, help='output histogram file')
parser.add_argument('--bins', '-b', type=int, default=30, help='number of bins for histogram')
parser.add_argument('--text', '-t', action='store_true', help='write histogram text file')

args = parser.parse_args()

C = pd.read_csv(args.input, index_col=0)
C = C.values
C = np.tril(C, k=-1).flatten()
mu = np.mean(C)
sigma = np.std(C)
print('mean:', mu)
print('stddev:', sigma)
if not args.text:
    plt.hist(C, bins=args.bins)
    plt.xlabel('Correlation')
    plt.ylabel('Count')
    # annotate mean and stddev
    plt.text(0.8, 0.8,f'mean: {round(mu,2)}', transform=plt.gca().transAxes)
    plt.text(0.8, 0.7,f'stddev: {round(sigma,2)}', transform=plt.gca().transAxes)
    # min and max
    plt.text(0.8,0.6, f'min: {round(np.min(C),2)}', transform=plt.gca().transAxes)
    plt.text(0.8,0.5, f'max: {round(np.max(C),2)}', transform=plt.gca().transAxes)
    # median
    plt.text(0.8,0.4, f'median: {round(np.median(C),2)}', transform=plt.gca().transAxes)
    plt.savefig(args.output)
    plt.close()
else:
    with open(args.output, 'w') as f:
        f.write('mean: {:.2f}\n'.format(mu))
        f.write('stddev: {:.2f}\n'.format(sigma))
        for i in range(len(C)):
            f.write('{}\n'.format(C[i]))
    

