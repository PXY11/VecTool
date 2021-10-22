# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 10:07:26 2021

@author: YS
"""

from indicatorTool import *

'''
用于测试indicatorTool
'''

updater_csi = Updater(instanceId=1)
res_csi = updater_csi.get_new(factor='csi',
                                  SignalCalculatorparamVersion='_v1',
                                  SignalCalculatoremark='_csi',
                                  save=False,
                                  upload = False,
                                  tableNameExt='BBELB')

updater_roc = Updater(instanceId=2)
res_roc = updater_roc.get_new(factor='roc',
                                 SignalCalculatorparamVersion='_v1',
                                 SignalCalculatoremark='_roc',
                                 save=False,
                                 upload=False,
                                 tableNameExt='BBELB')

updater_cci = Updater(instanceId=3)
res_cci = updater_cci.get_new(factor='cci',
                                 SignalCalculatorparamVersion='_v1',
                                 SignalCalculatoremark='_cci',
                                 save=False,
                                 upload=False,
                                 tableNameExt='BBELB')
#%%
updater_ar = Updater(instanceId=4)
res_ar = updater_ar.get_new(factor='absorptionRatio',
                                SignalCalculatorparamVersion='_v1',
                                SignalCalculatoremark='_ar',
                                save=False,
                                upload=False,
                                tableNameExt='BBELB')


updater_er = Updater(instanceId=5)
res_er = updater_er.get_new(factor='efficiencyRatio',
                                SignalCalculatorparamVersion='_v1',
                                SignalCalculatoremark='_er',
                                save=False,
                                upload=False,
                                tableNameExt='BBELB')
                                  
                                    
                                    
                                    
