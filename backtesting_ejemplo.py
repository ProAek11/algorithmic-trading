import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from Easy_Trading import Basic_funcs
import MetaTrader5 as mt5

nombre = 67043467
clave = 'Genttly.2022'
servidor = 'RoboForex-ECN'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

bfs = Basic_funcs(nombre, clave, servidor, path)

def get_datafeed(timeframe,symbol,cantidad):
    mt5.initialize( login = nombre, server = servidor, password = clave, path = path)
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, cantidad)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    data = rates_frame.copy()
    data = data.iloc[:,[0,1,2,3,4,5,7]]
    data.columns = ['time','Open','High','Low','Close','Volume','OpenInterest']
    data = data.set_index('time')

    return data


class Estrategia_simple(Strategy):
    def init(self):

        self.prices = self.I(lambda: np.repeat(np.nan, len(self.data)), name='prices')

    def next(self):
        self.prices = self.data.Close

        if len(self.data.Close) > 3:
            self.delta1 = self.prices[-1] - self.prices[-2]
            self.delta2 = self.prices[-2] - self.prices[-3]
            self.tps = self.prices[-1] + 0.01

            if (self.delta1 > 0) and (self.delta2 > 0):
                self.buy(tp = self.tps )
            if (self.delta1 < 0) and (self.delta2 < 0):
                self.sell(tp = self.prices[-1] - 0.01)

data = get_datafeed(mt5.TIMEFRAME_M1,'XAUUSD',200)
bt = Backtest(data,Estrategia_simple, cash= 10_000)
stats1 = bt.run()
bt.plot()