from os import close
from pickle import FALSE
import sys
sys.path.append('../../')
from vector import portfolio
import pandas as pd
from datetime import datetime, timedelta

class Trader(portfolio.Portfolio):
    def init(self, symbols: list):
        super().init(symbols)
        self.order_ids = {}
        for symbol in symbols:
            self.order_ids[symbol] = ""
        self.symbols = symbols
        self.init_cash = 100000
    
    def algorithm(self,s:dict):
        # er_dict_old = {} # {('sol', 'er'): 0.15652913653764372, ('ftm', 'er'): 0.06968790081231274......
        er_dict = {}
        for symbol in self.symbols:
            er_dict[symbol] = s[symbol]['er']
        er_list = sorted(er_dict.items(), key=lambda item:item[1]) #[(symbol,er)]
        er_max_symbols = [er_list[-1][0],er_list[-2][0]] #ER最大的一个币种
        er_max_symbols = [er_list[-1][0]]
        # er_threshold = sum([er_list[i][1] for i in range(len(er_list))])/len(er_list)
        # er_threshold = er_list[3][1] #er_threshold为全品种的er中位数

        for symbol in er_max_symbols:
            '''
            对于er最大的前1（2）个币种，若满足
            1、DEMA大于VWAP
            2、er大于avg序列历史平均值
            3、进一步可以改为total序列历史平均值 total意味着每个币种独自的平均
            '''
            signal_open = s[symbol]['DEMAoverVWAP']
            price = s[symbol]['close']
            time = s['datetime']
            if not self.order_ids[symbol]:
                if signal_open == True: #信号进
                    print(time,f'【{symbol}】DEMA is 【OVER】 VWAP and its ER is big, Long it.')
                    order_id = self.entry_order(symbol,round(1*self.init_cash/price, 2))
                    self.order_ids[symbol] = order_id
        
        for symbol in self.symbols:
            '''
            对于所有币种，检查是否有持仓，进一步判断
            1、er小于er_threshold，平仓
            2、信号变为False，平仓
            '''           
            if self.order_ids[symbol]:
                # if er_dict[symbol] < er_threshold:
                #     print(f'{symbol} is held,【er lower than er_threshold】, close order', self.order_ids[symbol])
                #     op = self.get_order(self.order_ids[symbol])
                #     self.exit_order(op)
                signal_close = s[symbol]['DEMAoverVWAP']
                if signal_close == False: #信号出
                    print(f'{symbol} is held,【siganl change to False】, close order ', self.order_ids[symbol])
                    # print('closeOrder',self.order_ids[symbol])
                    op = self.get_order(self.order_ids[symbol])
                    self.exit_order(op)
                    
    def on_order(self, order: portfolio.Order):
        if order.status == portfolio.OrderStatus.Finished:
            self.order_ids[order.symbol] = ""




