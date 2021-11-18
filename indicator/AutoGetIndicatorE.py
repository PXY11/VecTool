
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

updater_cci = Updater(DataToolparamVersion = '_v17',DataToolremark = '_E',instanceId=3)
res_cci = updater_cci.get_new(factor='cci',
                                 SignalCalculatorparamVersion='_v17',
                                 SignalCalculatoremark='_cci',
                                 save=True,
                                 upload=False,
                                 tableNameExt='E')

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
                                  

#updater_udp = Updater(DataToolparamVersion = '_v15',DataToolremark = '_BBELB',instanceId=11)
#res_udp = updater_udp.get_new(factor='updownPercent',
#                                SignalCalculatorparamVersion='_v15',
#                                SignalCalculatoremark='_udp',
#                                save=True,
#                                upload=False,
#                                tableNameExt='BBELB')

#%%
#pv = res_udp['total_result']
#pv_1d = pv
