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
        ar = s['ind']['ar']
        arRollNorm = s['ind']['arRollNorm']

        for symbol in ['eth']:
            '''
            对于btc币种，若满足
            1、arRollNorm 小于10时就做多
            '''
            signal_open = arRollNorm <= 15
            price = s[symbol]['close']
            time = s['datetime']
            if not self.order_ids[symbol]: #判断有无持仓
                if signal_open == True: #信号进
                    print(time,f'【{symbol}arRollNorm is 【OVER】 10, Long it.')
                    order_id = self.entry_order(symbol,round(1*self.init_cash/price, 2))
                    self.order_ids[symbol] = order_id

        signal_close = arRollNorm > 15
        for symbol in ['eth']:
            '''
            对于btc币种，检查是否有持仓，进一步判断
            1、arRollNorm 大于10时就空仓
            '''
            if self.order_ids[symbol]: #判断有无持仓
                if signal_close == True:
                    print(f'{symbol} is held,【siganl change to False】, close order ', self.order_ids[symbol])
                    op = self.get_order(self.order_ids[symbol])
                    self.exit_order(op)
    
    def on_order(self, order: portfolio.Order):
        if order.status == portfolio.OrderStatus.Finished:
            self.order_ids[order.symbol] = ""