import sys
sys.path.append('../')
sys.path.append('../../')
import ARTrader_v3
from vector import portfolio, data_source
import importlib
import talib as ta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import htmlplot
from scipy import stats
importlib.reload(portfolio)
importlib.reload(ARTrader_v3)
importlib.reload(htmlplot.core)
VERSION = '_v3'
SAVE = True
DRAWHOLDLINE = False #控制画持仓曲线
ar_params = [72,144,288,864,1440]
# ar_param = 864
winsizes = [24*12,24*18,24*24,24*36,24*48]
#winsize = 24*30
symbols = ["bnb", "btc", "eth", "ltc", "bch"]
result = []
#读取数据 #####################################################################
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
symbolSigDataAR = load_obj('ARdata/symbolsSigAvg_2018050120211124_60min_v18_ar')['60min']
simbolSigPV = load_obj('ARdata/symbolsData_2018032120211124_60min_v18_BBELB')['60min']
simbolSigPV = simbolSigPV.loc[symbolSigDataAR.index] #用信号时间索引截取行情数据
print('Read data done')

# AR Rolling Normalization ####################################################
def normalizationProcess(dataArray):
    q75 = np.quantile(dataArray, 0.75)
    q50 = np.quantile(dataArray, 0.5)
    q25 = np.quantile(dataArray, 0.25)
    scaleResult = 100*stats.norm.cdf(0.5*(dataArray[-1]-q50)/(q75-q25))-50
    return scaleResult

def get_ar_norm(df,arCol,WinSize):
    arRollNorm = df[arCol].dropna().rolling(WinSize).apply(normalizationProcess)
    return arRollNorm

for ar_param in ar_params:
    for winsize in winsizes:
        symbolSigDataAR[f'arRollNorm{winsize}'] = get_ar_norm(symbolSigDataAR,f'ar{ar_param}',winsize)
        symbolSigDataARRollNorm = symbolSigDataAR[[f'ar{ar_param}',f'arRollNorm{winsize}']]
        symbolSigDataARRollNorm = symbolSigDataARRollNorm.dropna(how='any')
        
        # 构造传入引擎的bar ############################################################
        symbolSig2BarDataARRollNorm = symbolSigDataARRollNorm.copy(deep=True)
        symbolSig2BarDataARRollNorm.columns = ['ar','arRollNorm'] #重命名用于构造bar的指标列名
        symbolSig2BarDataARRollNorm.columns = pd.MultiIndex.from_product([['ind'],['ar', 'arRollNorm']])
        simbolSig2BarPV = simbolSigPV.loc[symbolSig2BarDataARRollNorm.index]
        bars = simbolSig2BarPV.merge(symbolSig2BarDataARRollNorm,left_index=True,right_index=True)
        bars_test = bars.iloc[:]
        
        # 回测 ########################################################################
        trader = ARTrader_v3.Trader()
        balance = trader.backtest(bars_test,symbols)
        orders=trader.history_orders()
        trader.cal_period_performance(bars_test)
        res = trader.get_period_statistics(init_cash=int(1e7),freq='d')
        result.append(('ar_param',ar_param,'winsize',winsize,res[1]))
        # 绩效画图 ####################################################################
        ax = res[0]['balance'].iloc[:].plot(figsize=(15,7),\
                title='ar_param'+str(ar_param)+'winsize'+str(winsize)+' AnnualReturn'+str(res[1]['annualizedReturn']))
        fig = ax.get_figure()
        if SAVE == True:
            fig.savefig(f'./pic/ar{VERSION}/'+'ar_param'+str(ar_param)+'winsize'+str(winsize)+'.png')
        plt.show()

        orders=trader.history_orders()
        if DRAWHOLDLINE == True:
            for symbol in ['eth']:
                mp = htmlplot.core.MultiPlot(f'E:/ar{VERSION}/'+'ar_param'+str(ar_param)+'winsize'+str(winsize)+f'{symbol}.html')
                mp.set_main(bars[symbol], orders[orders.symbol==symbol])
                mp.show()
#%%
def perf_output(result:list,sample_num:int,name:str):
    rows = {}
    name = name
    for tpnum in ar_params[:sample_num]:
        tmp_row = [tup[4][name] for tup in result if tup[1]==tpnum]
        rows[tpnum] = tmp_row
    nameDF = pd.DataFrame(rows)
    nameDF.index = winsizes[:sample_num] #列索引是tp_param，行索引是er_param
    nameDF.to_csv(f'./perf/perf_ar{VERSION}/{name}.csv')
    return nameDF

df_max_rawdown = perf_output(result,5,'maxDrawdown')
df_annual_rtn = perf_output(result,5,'annualizedReturn')
df_sharpe = perf_output(result,5,'sharpeRatio')

