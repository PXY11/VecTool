import sys
sys.path.append('../')
sys.path.append('../../')
import ERMATrader
from vector import portfolio, data_source
import importlib
import talib as ta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import htmlplot
importlib.reload(portfolio)
importlib.reload(ERMATrader)
importlib.reload(htmlplot.core)
def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
version='_v2'
symbolSigDataTotalER = load_obj('../../data/symbolsSig/symbolsSigTotal_2021050120211028_5min_v3_er')['5min']
print('Read data done')
symbols = ["sol","ftm","uni","doge","fil","xlm","shib"]
pv = ['open','high','low','close','volume']
er = ['er18','er36','er72','er144','er288','er864','er1440','er2016','er2880']
tp_param = [18,36,72,144,288,864,1440,2016,2880]
er_param = [18,36,72,144,288,864,1440,2016,2880]
symbolsPV = symbolSigDataTotalER.loc[:, pd.IndexSlice[symbols, pv]]
#symbolsER = symbolSigDataTotalER.loc[:, pd.IndexSlice[symbols, er]]
symbolsClose = symbolSigDataTotalER.loc[:, pd.IndexSlice[symbols, "close"]]
symbolsClose.columns = symbols
symbolsVolume = symbolSigDataTotalER.loc[:, pd.IndexSlice[symbols, "volume"]]
symbolsVolume.columns = symbols
AnnualRtn = []
result = []
sample_num = 9
###############################################################################
for tp_parameter in tp_param[:sample_num]: #864
    for er_parameter in er_param[:sample_num]: #
        symbolsVWAP = pd.DataFrame()
        symbolsDEMA = pd.DataFrame()
        symbolsSigMA = pd.DataFrame()
        for col in symbols:
            symbolsVWAP[(col,'VWAP')] = ta.SUM(symbolsClose[col].values\
                                *symbolsVolume[col].values, timeperiod=tp_parameter)\
                                /ta.SUM(symbolsVolume[col].values, timeperiod=tp_parameter)
            symbolsDEMA[(col,'DEMA')] = ta.DEMA(symbolsClose[col].values,timeperiod=tp_parameter)
            symbolsSigMA[(col,'DEMAoverVWAP')] = symbolsDEMA[(col,'DEMA')]>symbolsVWAP[(col,'VWAP')]
        
        symbolsSigMA.index = symbolsPV.index
        bars = symbolsPV.merge(symbolsSigMA,left_index=True,right_index=True)
        symbolsSigER = symbolSigDataTotalER.loc[:, pd.IndexSlice[symbols, 'er'+str(er_parameter)]] ###ER72的数据
        symbolsSigER.columns = [(tup[0],tup[1][:2]) for tup in symbolsSigER.columns.tolist()] #重命名er的列
        bars = bars.merge(symbolsSigER,left_index=True,right_index=True) ###拼接进去的是ER72的数据
        #s = bars.iloc[0,:].to_dict() 
        trader = ERMATrader.Trader()  #实例化Trader类时不需要传入参数 
        bars_test = bars.iloc[:,:]
        balance = trader.backtest(bars_test, symbols) #传入的bar就是run2计算好的signal，传入的symbols是对应的币种list
        # 获取 order
        orders=trader.history_orders()
        print('*****************************【订单】***************************** \n',orders)
        trader.cal_period_performance(bars)
        res = trader.get_period_statistics(init_cash=100000,freq='d')
        result.append(('tp',tp_parameter,'er',er_parameter,res[1]))
        #绩效画图并保存
        ax = res[0]['balance'].iloc[:].plot(figsize=(15,7),\
                title='tp'+str(tp_parameter)+'er'+str(er_parameter)+' AnnualReturn'+str(res[1]['annualizedReturn']))
        fig = ax.get_figure()
        fig.savefig(f'./pic{version}/'+'tp'+str(tp_parameter)+'er'+str(er_parameter)+'.png')
        plt.show()
        orders=trader.history_orders()
#        mp = htmlplot.core.MultiPlot()
#        mp.set_main(bars["sol"], orders[orders.symbol=="sol"])
#        mp.show()
        print('annualizedReturn: ',res[1]['annualizedReturn'])
        AnnualRtn.append(
                         ('tp',tp_parameter,'er',er_parameter,str(res[1]['annualizedReturn']))
                         )

def perf_output(result:list,sample_num:int,name:str):
    rows = {}
    name = name
    for tpnum in tp_param[:sample_num]:
        tmp_row = [tup[4][name] for tup in result if tup[1]==tpnum]
        rows[tpnum] = tmp_row
    nameDF = pd.DataFrame(rows)
    nameDF.index = er_param[:sample_num] #列索引是tp_param，行索引是er_param
    nameDF.to_csv(f'./perf{version}/{name}.csv')

for key in result[0][4].keys():
    perf_output(result,sample_num,key)