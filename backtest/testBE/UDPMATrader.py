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
        # er_dict = {}
        # for symbol in self.symbols:
        #     er_dict[symbol] = s[symbol]['er']
        # er_list = sorted(er_dict.items(), key=lambda item:item[1]) #[(symbol,er)]
        # er_max_symbols = [er_list[-1][0]]
        # # er_threshold = sum([er_list[i][1] for i in range(len(er_list))])/len(er_list)
        # # er_threshold = er_list[3][1] #er_threshold为全品种的er中位数
        udp_key = list(s.keys())[-2]
        udp = s[udp_key][""]
        # print('此个bar中的udp_key: ',udp_key)
        # print('此个bar中的s: ',s)
        for symbol in self.symbols:
            '''
            对BTC和ETH检查其是否满足MA条件，以及此个bar中udp是否满足大于0的条件
            '''
            signal_open = s[symbol]['CLOSEoverMA']
            price = s[symbol]['close']
            time = s['datetime']
            if not self.order_ids[symbol]:
                if signal_open == True and udp > 0 : #信号进
                    
                    print(time,f'【{symbol}】CLOSE is 【OVER】 MA and UDP is 【POSITIVE】, Long it.')
                    order_id = self.entry_order(symbol,round(1*self.init_cash/price, 2))
                    self.order_ids[symbol] = order_id
        
        for symbol in self.symbols:
            '''
            对于所有币种，检查是否有持仓，进一步判断
            1、信号变为False，平仓
            '''           
            if self.order_ids[symbol]:
                signal_close = s[symbol]['CLOSEoverMA']
                if signal_close == False or udp <= 0: #信号出
                    print(f'{symbol} is held,【siganl change to False】, close order ', self.order_ids[symbol])
                    op = self.get_order(self.order_ids[symbol])
                    self.exit_order(op)
                    
    def on_order(self, order: portfolio.Order):
        if order.status == portfolio.OrderStatus.Finished:
            self.order_ids[order.symbol] = ""




