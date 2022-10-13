import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from Easy_Trading import Basic_funcs
import MetaTrader5 as mt5
import pandas_ta as ta
from backtesting.lib import crossover


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
    n1 =20
    n2 = 40
    
    def init(self):

        self.prices = self.I(lambda: np.repeat(np.nan, len(self.data)), name='prices')

    def next(self):
        self.prices = self.data.Close

        if len(self.data.Close) > 3:
            self.delta1 = self.prices[-1] - self.prices[-2]
            self.delta2 = self.prices[-2] - self.prices[-3]
            self.tps = self.prices[-1] + 0.01

            if (self.delta1 > 0) and (self.delta2 > 0):
                self.position.close()
                self.buy(tp = self.tps )
            if (self.delta1 < 0) and (self.delta2 < 0):
                self.position.close()
                self.sell(tp = self.prices[-1] - 0.01)

data = get_datafeed(mt5.TIMEFRAME_M1,'XAUUSD',400)
bt = Backtest(data,Estrategia_simple, cash= 10_000)
stats1 = bt.run()
bt.plot()



class Estrategia_cruce_medias(Strategy):
    n1 =20
    n2 = 40
    
    def init(self):

        prices = self.data.Open
        self.ma20 = self.I(ta.sma,pd.Series(prices),self.n1)
        self.ma40 = self.I(ta.sma,pd.Series(prices),self.n2)           

    def next(self):
        
        if len(self.data.Open) > 40:
            if crossover(self.ma20, self.ma40):
                self.position.close()
                self.buy( )
            if crossover(self.ma40,self.ma20):
                self.position.close()
                self.sell()

data = get_datafeed(mt5.TIMEFRAME_M1,'XAUUSD',99000)
bt = Backtest(data,Estrategia_cruce_medias, cash= 10_000)
stats1 = bt.run()
bt.plot()

class Estrategia_medias_rsi(Strategy):
    n1 =20
    prsi = 14
    lim_sup_rsi = 70
    lim_inf_rsi = 30
    
    def init(self):

        prices = self.data.Open
        self.ma20 = self.I(ta.sma,pd.Series(prices),self.n1)
        self.rsi = self.I(ta.rsi,pd.Series(prices),self.prsi)           

    def next(self):
        
        if len(self.data.Open) > 21:
            if (self.rsi > self.lim_sup_rsi) and (self.ma20[-1] - self.ma20[-2] < 0):
                self.position.close()
                self.sell( )
            if (self.rsi < self.lim_inf_rsi) and (self.ma20[-1] - self.ma20[-2] > 0):
                self.position.close()
                self.buy()

data = get_datafeed(mt5.TIMEFRAME_M1,'XAUUSD',99000)
bt = Backtest(data,Estrategia_medias_rsi, cash= 10_000)
stats1 = bt.run()
bt.plot()

stats1, hm = bt.optimize(n1 = [5,10,20],
                        prsi = [10,11,14],
                        lim_sup_rsi = [70,75,80],
                        lim_inf_rsi = [30,25,20], return_heatmap=True,
                        maximize = 'Win Rate [%]')