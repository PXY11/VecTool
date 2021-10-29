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
        er_dict = {} 
        for symbol in self.symbols:
            er_dict[(symbol,'er')] = s[symbol]['er'] #取出 ER dict
        er_list = sorted(er_dict.items(), key=lambda item:item[1]) #按照value对字典升序排列
        er_max_symbols = [er_list[-1][0][0],er_list[-2][0][0]] #ER最大的两个币种

        for symbol in er_max_symbols:
            signal = s[symbol]['DEMAoverVWAP']
            price = s[symbol]['close']
            time = s['datetime']
            if not self.order_ids[symbol]:
                if signal == True:
                    # print(time,f'【{symbol}】DEMA is below VWAP and its ER is big, Short it.')
                    # order_id = self.entry_order(symbol,round(-1*self.init_cash/price, 2))
                    print(time,f'【{symbol}】DEMA is 【OVER】 VWAP and its ER is big, Long it.')
                    order_id = self.entry_order(symbol,round(1*self.init_cash/price, 2))
                    self.order_ids[symbol] = order_id
                    # self.set_trailing_stop(order_id,0.2,s[symbol]['low'])

                # elif signal == False:
                #     print(time,f'【{symbol}】DEMA is 【below】 VWAP and its ER is big, Short it.')
                #     order_id = self.entry_order(symbol,round(-1*self.init_cash/price, 2))
                #     self.order_ids[symbol] = order_id

            elif self.order_ids[symbol]:
                if signal == False:
                    print('closeOrder',self.order_ids[symbol])
                    op = self.get_order(self.order_ids[symbol])
                    self.exit_order(op)
    
    def on_order(self, order: portfolio.Order):
        if order.status == portfolio.OrderStatus.Finished:
            self.order_ids[order.symbol] = ""




