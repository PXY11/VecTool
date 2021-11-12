import sys
sys.path.append('../')
sys.path.append('../../')
import UDPMATrader
from vector import portfolio, data_source
import importlib
import talib as ta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import htmlplot
importlib.reload(portfolio)
importlib.reload(UDPMATrader)
importlib.reload(htmlplot.core)
version = '_v1'
save = False
drawHoldLine = False #控制画持仓曲线
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
symbolSigDataTotalUDP = load_obj('../../data/symbolsSig/symbolsSigTotal_2018050220211110_1440min_v15_udp')['1440min']
symbolSigDataAvgUDP = load_obj('../../data/symbolsSig/symbolsSigAvg_2018050220211110_1440min_v15_udp')['1440min']
print('Read data done')
symbols = ["btc", "eth"]
pv = ['open','high','low','close','volume']
udp_param = [20,30,40,50,60,70,80,90,100]
symbolsPV = symbolSigDataTotalUDP.loc[:, pd.IndexSlice[symbols, pv]]
symbolsClose = symbolSigDataTotalUDP.loc[:, pd.IndexSlice[symbols, "close"]]
symbolsClose.columns = symbols
symbolsVolume = symbolSigDataTotalUDP.loc[:, pd.IndexSlice[symbols, "volume"]]
symbolsVolume.columns = symbols
AnnualRtnSharpe = []
result = []
sample_num = 9
###############################################################################
#for tp_parameter in tp_param[:1]: #
for udp_parameter in udp_param[:]: #
    tp_parameter = udp_parameter
    symbolsVWAP = pd.DataFrame()
    symbolsDEMA = pd.DataFrame()
    symbolsSigMA = pd.DataFrame()
    symbolsMA = pd.DataFrame()
    symbolsCLOSE = pd.DataFrame()
    for col in symbols:
        symbolsMA[(col,'MA')] = ta.MA(symbolsClose[col].values,timeperiod=tp_parameter)
        symbolsCLOSE[(col,'CLOSE')] = ta.MA(symbolsClose[col].values,timeperiod=1)
        symbolsSigMA[(col,'CLOSEoverMA')] = symbolsCLOSE[(col,'CLOSE')] > symbolsMA[(col,'MA')] 
    symbolsSigMA.index = symbolsPV.index
    bars = symbolsPV.merge(symbolsSigMA,left_index=True,right_index=True)
    symbolsSigUDP = symbolSigDataAvgUDP.loc[:, [('udp'+str(udp_parameter),'')]] 
    symbolsSigUDP.columns = [(tup[0],tup[1][:2]) for tup in symbolsSigUDP.columns.tolist()] #重命名er的列
    bars = bars.merge(symbolsSigUDP,left_index=True,right_index=True) ###拼接进去的是ER的数据
    ###########################################################################
    symbolsMA.index = symbolsPV.index
    df_eda = bars.merge(symbolsMA,left_index=True,right_index=True)
    ###########################################################################
    trader = UDPMATrader.Trader()
    barsNum = 0 #设置参数，选择回测日期
    bars_test = bars.iloc[-barsNum:,:] #设置参数，选择回测日期
    balance = trader.backtest(bars_test, symbols) #传入的bar就是run2计算好的signal，传入的symbols是对应的币种list
    # 获取 order
    orders=trader.history_orders()
    print('*****************************【订单】***************************** \n',orders)
    trader.cal_period_performance(bars)
    res = trader.get_period_statistics(init_cash=int(1e7),freq='d')
    result.append(('tp',tp_parameter,udp_parameter,res[1]))
    #绩效画图并保存
    ax = res[0]['balance'].iloc[-barsNum:].plot(figsize=(15,7),\
            title='tp'+str(tp_parameter)+' AnnualReturn'+str(res[1]['annualizedReturn']))
    fig = ax.get_figure()
    if save == True:
        fig.savefig(f'./pic/pic{version}/'+'tp'+str(tp_parameter)+'.png')
    plt.show()
    orders=trader.history_orders()
    
    if drawHoldLine == True:
        for symbol in symbols[:]:
            mp = htmlplot.core.MultiPlot('E:/htmlBE/'+'tp'+str(tp_parameter)+f'{symbol}.html')
            mp.set_main(bars[symbol], orders[orders.symbol==symbol])
            mp.show()
    
    print('annualizedReturn: ',res[1]['annualizedReturn'])
    AnnualRtnSharpe.append(
                     ('tp',tp_parameter,str(res[1]['annualizedReturn']),str(res[1]['sharpeRatio']))
                     )
#%%
ls_artns = [tu[2] for tu in AnnualRtnSharpe]
ls_sharpes = [tu[3] for tu in AnnualRtnSharpe]
ls_tp = [tu[1] for tu in AnnualRtnSharpe]
df_perf = pd.DataFrame({'tp':ls_tp,'annual return':ls_artns,'sharpe ratio':ls_sharpes})
#%%
##%%
#sample_num = 9
#def perf_output(result:list,sample_num:int,name:str):
#    rows = {}
#    name = name
#    for tpnum in tp_param[:sample_num]:
#        tmp_row = [tup[4][name] for tup in result if tup[1]==tpnum]
#        rows[tpnum] = tmp_row
#    nameDF = pd.DataFrame(rows)
#    nameDF.index = udp_param[:sample_num] #列索引是tp_param，行索引是udp_param
#    nameDF.to_csv(f'./perf/perf{version}/{name}.csv')
#    
#if save == True:
#    for key in result[0][4].keys():
#        perf_output(result,sample_num,key)