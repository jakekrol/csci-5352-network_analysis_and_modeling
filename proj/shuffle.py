#!/usr/bin/env python3
import numpy as np
import pandas as pd
import argparse

# input data matrix
# output shuffled data matrix

# args
parser = argparse.ArgumentParser(description='Shuffle Data Matrix')
parser.add_argument('--input', '-i', type=str, required=True, help='input data matrix file')
parser.add_argument('--output', '-o', type=str, required=True, help='output shuffled data matrix file')
parser.add_argument('--seed', '-s', type=int, default=42, help='random seed for shuffling')
parser.add_argument('--shuffles', '-n', type=int, default=1000, help='number of shuffles to perform')
args = parser.parse_args()

# read
df = pd.read_csv(args.input)
columns = df.columns
A = df.values
# shuffle
rng = np.random.default_rng(seed=args.seed)
for i in range(args.shuffles):
    A_f = A.flatten()
    rng.shuffle(A_f)  # shuffle in-place
    A = A_f.reshape(A.shape)
    print(i)
# write
A = pd.DataFrame(A, columns=columns)
A.to_csv(args.output, index=False)

