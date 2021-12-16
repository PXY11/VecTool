
from indicatorTool import *

'''
用于测试indicatorTool
'''

#updater_csi = Updater(DataToolparamVersion = '_v3',DataToolremark = '_SFUDFX',instanceId=1)
#res_csi = updater_csi.get_new(factor='csi',
#                                  SignalCalculatorparamVersion='_v3',
#                                  SignalCalculatoremark='_csi',
#                                  save=False,
#                                  upload = False,
#                                  tableNameExt='SFUDFX')
#


#updater_roc = Updater(DataToolparamVersion = '_v3',DataToolremark = '_SFUDFX',instanceId=2)
#res_roc = updater_roc.get_new(factor='roc',
#                                 SignalCalculatorparamVersion='_v3',
#                                 SignalCalculatoremark='_roc',
#                                 save=False,
#                                 upload=False,
#                                 tableNameExt='SFUDFX')
#
# updater_cci = Updater(DataToolparamVersion = '_v16',DataToolremark = '_E',instanceId=3)
# res_cci = updater_cci.get_new(factor='cci',
#                                  SignalCalculatorparamVersion='_v16',
#                                  SignalCalculatoremark='_cci',
#                                  save=True,
#                                  upload=False,
#                                  tableNameExt='E')


# updater_ar = Updater(DataToolparamVersion = '_v13',DataToolremark = '_BBELB',instanceId=13)
# res_ar = updater_ar.get_new(factor='absorptionRatio',
#                                SignalCalculatorparamVersion='_v13',
#                                SignalCalculatoremark='_ar',
#                                save=True,
#                                upload=True,
#                                tableNameExt='BBELB')
                       
                                    
#updater_er = Updater(DataToolparamVersion = '_v9',DataToolremark = '_BBELB',instanceId=5)
#res_er = updater_er.get_new(factor='efficiencyRatioSign',
#                                SignalCalculatorparamVersion='_v9',
#                                SignalCalculatoremark='_ersign',
#                                save=False,
#                                upload=False,
#                                tableNameExt='BBELB')
                                  

# updater_udp = Updater(DataToolparamVersion = '_v19',DataToolremark = '_BEMULA',instanceId=11)
# res_udp = updater_udp.get_new(factor='updownPercent',
#                                 SignalCalculatorparamVersion='_v19',
#                                 SignalCalculatoremark='_udp',
#                                 save=False,
#                                 upload=False,
#                                 tableNameExt='BEMULA')

updater_udp_60min = Updater(DataToolparamVersion = '_v20',DataToolremark = '_BEMULA',instanceId=19)
res_udp_60min = updater_udp_60min.get_new(factor='updownPercent',
                                SignalCalculatorparamVersion='_v20',
                                SignalCalculatoremark='_udp',
                                save=False,
                                upload=False,
                                tableNameExt='BEMULA')

#%%
#计算volatility
import talib as ta
import matplotlib.pyplot as plt
pv = res_udp_60min['total_result']
close = pv.loc[:, [('btc', 'close'),('eth', 'close'),('matic', 'close'),\
                    ('uni', 'close'),('link', 'close'),('axs', 'close')]]
symbols = ['btc','eth','matic','uni','link','axs']
pctChange = pd.DataFrame()
vol = pd.DataFrame()
for symbol in symbols:
    pctChange[symbol] = close.loc[:,(symbol,'close')].pct_change()
    vol[symbol] = ta.STDDEV(pctChange[symbol], 24*5)*(24**0.5)
#%%
#画相关性热力图
import seaborn as sns
corr = pctChange.iloc[-6*24:,:].corr()
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True
for i in range(len(mask)):
    mask[i,i] = 0
with sns.axes_style("white"):
    ax = sns.heatmap(corr, mask=mask,square=True,annot=True,cmap="YlGnBu")
eth_avg_corr = ((corr.sum()-1)/5)['eth']
eth_avg_corr = round(eth_avg_corr,2)
plt.text(-1,-1,f'The last 6 days HOUR\'s RETURN array average CORRELATION')
plt.text(-1,-0.6,f'between ETH and others is : {eth_avg_corr}')
plt.show()


