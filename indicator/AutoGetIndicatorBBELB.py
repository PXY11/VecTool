
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
#updater_cci = Updater(DataToolparamVersion = '_v3',DataToolremark = '_SFUDFX',instanceId=3)
#res_cci = updater_cci.get_new(factor='cci',
#                                 SignalCalculatorparamVersion='_v3',
#                                 SignalCalculatoremark='_cci',
#                                 save=False,
#                                 upload=False,
#                                 tableNameExt='SFUDFX')
##%%
updater_ar = Updater(DataToolparamVersion = '_v13',DataToolremark = '_BBELB',instanceId=13)
res_ar = updater_ar.get_new(factor='absorptionRatio',
                                SignalCalculatorparamVersion='_v13',
                                SignalCalculatoremark='_ar',
                                save=True,
                                upload=True,
                                tableNameExt='BBELB')


# updater_er = Updater(DataToolparamVersion = '_v5',DataToolremark = '_BBELB',instanceId=5)
# res_er = updater_er.get_new(factor='efficiencyRatio',
#                                 SignalCalculatorparamVersion='_v5',
#                                 SignalCalculatoremark='_er',
#                                 save=True,
#                                 upload=False,
#                                 tableNameExt='BBELB')
                                  
                                    
                                    
                                    
#updater_er = Updater(DataToolparamVersion = '_v9',DataToolremark = '_BBELB',instanceId=5)
#res_er = updater_er.get_new(factor='efficiencyRatioSign',
#                                SignalCalculatorparamVersion='_v9',
#                                SignalCalculatoremark='_ersign',
#                                save=False,
#                                upload=False,
#                                tableNameExt='BBELB')
                                  