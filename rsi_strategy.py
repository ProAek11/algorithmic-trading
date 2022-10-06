from time import perf_counter
from backtesting import Backtest, Strategy
import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from sklearn.linear_model import LinearRegression
from scipy import stats
import pandas_ta as ta

nombre = 67043467
clave = 'Genttly.2022'
servidor = 'RoboForex-ECN'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

def get_datafeed(timeframe,symbol):
    mt5.initialize( login = nombre, server = servidor, password = clave, path = path)
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 99000)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
    data = rates_frame.copy()
    data = data.iloc[:,[0,1,2,3,4,5,7]]
    data.columns = ['time','Open','High','Low','Close','Volume','OpenInterest']
    data = data.set_index('time')

    return data

eurusd = get_datafeed(mt5.TIMEFRAME_M5,'AUDNZD')
eurusd2 = eurusd.copy()

eurusd2['rsi'] = ta.rsi(eurusd2['Close'],14)
sigma = eurusd2['rsi'].std()
mu = eurusd2['rsi'].mean()


class RSI_sigma(Strategy):
    t_sigma = 3.3
    tp_val = 0.006
    sl_val = 0.001
    def init(self):
        self.mu = 50.19
        self.sigma = 10.78
        self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), 14)

        

    def next(self):
        if len(self.data)>14:
            if self.rsi[-1] > mu + self.t_sigma*sigma:
                price = self.data.Close[-1]
                #self.position.close()
                self.sell(tp = price - self.tp_val, sl = price + self.sl_val)
            if self.rsi[-1] < mu - self.t_sigma*sigma:
                price = self.data.Close[-1]
                
                self.buy(tp = price + self.tp_val, sl = price - self.sl_val)

bt = Backtest(eurusd,RSI_sigma, cash = 10_000)

stats1, hm = bt.optimize( t_sigma = [2.5,2.6,2.7,2.8,2.9,3],
                          tp_val = [0.003,0.004,0.005,0.006,0.007],
                          sl_val = [0.003,0.002,0.001],
                     maximize = 'Win Rate [%]',
                     return_heatmap = True)

pairs = ['AUDNZD','CADCHF','GBPAUD','GBPCHF','EURNZD','AUDCAD','AUDCHF','GBPCAD','GBPNZD',
'NZDUSD']
results1 = []
for pair in pairs:
    eurusd = get_datafeed(mt5.TIMEFRAME_M1,pair)
    eurusd2 = eurusd.copy()

    eurusd2['rsi'] = ta.rsi(eurusd2['Close'],14)
    sigma = eurusd2['rsi'].std()
    mu = eurusd2['rsi'].mean()

    class RSI_sigma(Strategy):
        t_sigma = 3.3
        tp_val = 0.006
        sl_val = 0.001
        mus = 50
        sigmas = 10
        def init(self):
            
            self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), 14)

            

        def next(self):
            if len(self.data)>14:
                if self.rsi[-1] > self.mus + self.t_sigma*self.sigmas:
                    price = self.data.Close[-1]
                    #self.position.close()
                    self.sell(tp = price - self.tp_val, sl = price + self.sl_val)
                if self.rsi[-1] < self.mus - self.t_sigma*self.sigmas:
                    price = self.data.Close[-1]
                    
                    self.buy(tp = price + self.tp_val, sl = price - self.sl_val)
        
            
    bt = Backtest(eurusd,RSI_sigma, cash = 10_000)

    stats1, hm = bt.optimize( t_sigma = [2.5,2.6,2.7,2.8,2.9,3],
                            tp_val = [0.003,0.004,0.005,0.006,0.007],
                            sl_val = [0.003,0.002,0.001],
                            mus = mu,
                            sigmas = sigma,
                        maximize = 'Win Rate [%]',
                        return_heatmap = True)
    
    print(stats1)
    res = stats1._strategy
    results1.append(res)


    



