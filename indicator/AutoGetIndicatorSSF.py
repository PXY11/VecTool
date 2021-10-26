
from indicatorTool import *

'''
用于测试indicatorTool
'''

updater_csi = Updater(DataToolparamVersion = '_v2',DataToolremark = '_SSF',instanceId=1)
res_csi = updater_csi.get_new(factor='csi',
                                  SignalCalculatorparamVersion='_v2',
                                  SignalCalculatoremark='_csi',
                                  save=False,
                                  upload = False,
                                  tableNameExt='SSF')

updater_roc = Updater(DataToolparamVersion = '_v2',DataToolremark = '_SSF',instanceId=2)
res_roc = updater_roc.get_new(factor='roc',
                                 SignalCalculatorparamVersion='_v2',
                                 SignalCalculatoremark='_roc',
                                 save=False,
                                 upload=False,
                                 tableNameExt='SSF')

updater_cci = Updater(DataToolparamVersion = '_v2',DataToolremark = '_SSF',instanceId=3)
res_cci = updater_cci.get_new(factor='cci',
                                 SignalCalculatorparamVersion='_v2',
                                 SignalCalculatoremark='_cci',
                                 save=False,
                                 upload=False,
                                 tableNameExt='SSF')
#%%
updater_ar = Updater(DataToolparamVersion = '_v2',DataToolremark = '_SSF',instanceId=4)
res_ar = updater_ar.get_new(factor='absorptionRatio',
                                SignalCalculatorparamVersion='_v2',
                                SignalCalculatoremark='_ar',
                                save=False,
                                upload=False,
                                tableNameExt='SSF')


updater_er = Updater(DataToolparamVersion = '_v2',DataToolremark = '_SSF',instanceId=5)
res_er = updater_er.get_new(factor='efficiencyRatio',
                                SignalCalculatorparamVersion='_v2',
                                SignalCalculatoremark='_er',
                                save=False,
                                upload=False,
                                tableNameExt='SSF')
                                  
                                    
                                    
                                    
