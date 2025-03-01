#!/usr/bin/env python3
import networkx as nx
import pandas as pd
s = pd.read_csv('net1m_nodes.csv', delimiter=',', usecols=[3],comment='#',header=None).squeeze()
print(s.value_counts())
# 1: 908
# 2: 513

### hvr
#   33 1
#      24 2
#      40 3
#     176 4
#      21 5
#      13 6