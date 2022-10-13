import pandas as pd
import numpy as np
import pandas_ta as ta
from Easy_Trading import Basic_funcs
import MetaTrader5 as mt5
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

nombre = 67059268
clave = 'Inup.2022'
servidor = 'RoboForex-ECN'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'


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
    

eurusd = get_datafeed(mt5.TIMEFRAME_H1,'XAUUSD',99000)
eurusd2 = eurusd.copy()

eurusd2['sma'] = ta.sma(eurusd2['Close'],14)
eurusd2['devs'] = eurusd2['Close'] - eurusd2['sma']
sigma = eurusd2['devs'].std()
mu = eurusd2['devs'].mean()

def calculate_std(data,p_sma):
    sma = pd.Series(data['Close']).rolling(p_sma).mean()
    desv = pd.Series(data['Close']) - sma
    sigma = desv.std()
    

    return sigma

def calculate_mean(data,p_sma):
    sma = pd.Series(data['Close']).rolling(p_sma).mean()
    desv = pd.Series(data['Close']) - sma
    
    mu = desv.mean()

    return mu


class Desv_strategy(Strategy):
    t_sigma = 0.1
    tp_val = 0.9
    sl_val = 0.3
    p_sma = 14

    def init(self):
        # self.mu = 50.19
        # self.sigma = 10.78
        self.sma = self.I(ta.sma, pd.Series(self.data.Close), self.p_sma)
        self.desv = self.data.Close - self.sma
        mu = calculate_std(self.data,self.p_sma)
        sigma = calculate_mean(self.data,self.p_sma)
        print(type(self.desv))
        print(mu)
        print(sigma)

        

    def next(self):
        if len(self.data)>self.p_sma:
            if self.desv > mu + self.t_sigma*sigma:
                price = self.data.Close[-1]
                #self.position.close()
                self.sell(tp = price - self.tp_val, sl = price + self.sl_val)
            if self.desv < mu - self.t_sigma*sigma:
                price = self.data.Close[-1]
                self.buy(tp = price + self.tp_val, sl = price - self.sl_val)

bt = Backtest(eurusd,Desv_strategy, cash = 10_000)

stats1 = bt.run()

stats1, hm = bt.optimize( t_sigma = [2],
                          tp_val = [0.003,0.004,0.005],
                          sl_val = [0.003,0.002,0.001],
                          p_sma = [20],
                     maximize = 'Win Rate [%]',
                     return_heatmap = True)