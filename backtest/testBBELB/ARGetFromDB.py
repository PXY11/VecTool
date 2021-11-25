import pandas as pd
import numpy as np
import talib as ta
import os
import matplotlib.pyplot as plt
import warnings
import pymongo
from datetime import datetime

warnings.filterwarnings('ignore')

def prepareData(collection, startTime, endTime,rsPeriod=0):
    data_df = pd.DataFrame(
        list(collection.find({"datetime": {'$gt': startTime, '$lt': endTime}}))
    )
    data = data_df.copy()
    data = data.set_index('datetime')
    return data

symbol = 'absorptionRatioBBELB'
client = pymongo.MongoClient('172.16.11.81', 27017)
collection = client['multiSymbolsIndicator'][symbol]
startTime = datetime(2018, 5, 1)
endTime = datetime(2021,11,23)
dfAR = prepareData(collection, startTime, endTime)

#%%
import pickle
with open('ARfromDB/ar_2018050120211123_5min.pkl','wb') as f:
    pickle.dump(dfAR, f, pickle.HIGHEST_PROTOCOL)
#%%
with open('ARfromDB/ar_2018050120211123_5min.pkl','rb') as f:
    dfARlocal = pickle.load(f)