
from indicatorTool import *

'''
用于测试indicatorTool
'''

import talib as ta                             
import pandas as pd
updater_udp = Updater(DataToolparamVersion = '_v15',DataToolremark = '_BBELB',instanceId=11)
res_udp = updater_udp.get_new(factor='updownPercent',
                                SignalCalculatorparamVersion='_v15',
                                SignalCalculatoremark='_udp',
                                save=False,
                                upload=False,
                                tableNameExt='BBELB')
total_result = res_udp['total_result']
avg_result = res_udp['avg_result']
#%%
total_result['btcMA60'] = ta.MA(total_result.loc[:,('btc','close')], 60)
total_result['ethMA60'] = ta.MA(total_result.loc[:,('eth','close')], 60)
total_result['btcCloseOverMA60'] = total_result.loc[:,('btc','close')] > total_result.loc[:,('btcMA60','')]
total_result['ethCloseOverMA60'] = total_result.loc[:,('eth','close')] > total_result.loc[:,('ethMA60','')]

df_signal = total_result[['btcCloseOverMA60','ethCloseOverMA60']]

df_signal = df_signal.merge(avg_result[['udp60']],left_index=True,right_index=True)

df_signal.to_csv(r'D:\python_proj\UniST\data\btceth\df_signal.csv')





