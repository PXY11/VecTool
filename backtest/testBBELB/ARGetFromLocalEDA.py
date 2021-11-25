# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 14:03:55 2021

@author: YS
"""

import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
with open('ARdata/symbolsSigAvg_2018050120211124_60min_v18_ar.pkl','rb') as f:
    dfARlocal = pickle.load(f)['60min']
with open('ARdata/symbolsData_2018032120211124_5min_v13_BBELB.pkl','rb') as f:
    dfCoin = pickle.load(f)['5min']
# dfARlocal = dfARlocal[['ar18','ar36','ar72','ar144','ar288','ar864','ar1440','ar2016','ar2880']]
dfARlocal


from scipy import stats
def normalizationProcess(dataArray):
    q75 = np.quantile(dataArray, 0.75)
    q50 = np.quantile(dataArray, 0.5)
    q25 = np.quantile(dataArray, 0.25)
    scaleResult = 100*stats.norm.cdf(0.5*(dataArray[-1]-q50)/(q75-q25))-50
    return scaleResult

ar2880RollNorm = dfARlocal['ar2880'].dropna().rolling(720).apply(normalizationProcess)