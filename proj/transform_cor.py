#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os,sys
import argparse

parser = argparse.ArgumentParser(description='Transform correlation matrix values by 1 - |A_ij|')
parser.add_argument('-i', '--input', type=str, required=True, help='Input correlation matrix file')
parser.add_argument('-o', '--output', type=str, required=True, help='Output correlation matrix file')
args = parser.parse_args()

df = pd.read_csv(args.input, index_col=0)

df = df.map(lambda x: 1 - (abs(x)))
df.to_csv(args.output, index=True)
