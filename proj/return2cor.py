#!/usr/bin/env python3
import os,sys
import pandas as pd
import argparse

# input log return data matrix
# output correlation matrix
parser = argparse.ArgumentParser(description='Calculate Correlation Matrix')
parser.add_argument('--input', '-i', type=str, required=True, help='input log return data matrix file')
parser.add_argument('--output', '-o', type=str, required=True, help='output file')
args= parser.parse_args()

df_return = pd.read_csv(args.input)
cor = df_return.corr(method='pearson')
cor.to_csv(args.output, index=True)