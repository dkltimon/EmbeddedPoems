# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 03:12:21 2024

@author: KeliDu
"""

from statsmodels.stats import inter_rater as irr
import pandas as pd
import os
from collections import Counter

os.chdir(r'C:\Workstation\conferences\2025_DH')

#position: 0.87
df = pd.read_csv(r'position.csv', sep='\t')
dats, cats = irr.aggregate_raters(df)
irr.fleiss_kappa(dats, method='fleiss')

#perspective: 0.89
df = pd.read_csv(r'perspective.csv', sep='\t')
dats, cats = irr.aggregate_raters(df)
irr.fleiss_kappa(dats, method='fleiss')

#content: 0.66
df = pd.read_csv(r'content.csv', sep='\t')
dats, cats = irr.aggregate_raters(df)
irr.fleiss_kappa(dats, method='fleiss')


labels = []
x = 0
while x < len(df):
    row_count = Counter(df.loc[x])
    value, count = row_count.most_common()[0]
    if count > 1:
        labels.append(value)
    else:
        labels.append('check')
    x+=1





