from backtesting import Backtest, Strategy
import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from sklearn.linear_model import LinearRegression
from Easy_Trading import Basic_funcs
from scipy import stats


nombre = 67043467
clave = 'Genttly.2022'
servidor = 'RoboForex-ECN'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

bfs = Basic_funcs(nombre,clave,servidor,path)

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

def get_y(data):
    y = data.Close
    return y

eurusd = get_datafeed(mt5.TIMEFRAME_M1,'EURUSD')

class TestStrategy(Strategy):

    def init(self):
        self.coef = self.I(lambda: np.repeat(np.nan, len(self.data)), name='coef')
        self.p_value = self.I(lambda: np.repeat(np.nan, len(self.data)), name='p_value')
        
        

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.5f' % self.dataclose[0])
        # self.log(self.coef)
        per = 10
        if len(self.data) >= per:
            self.period = per
            X = np.array(range(self.period)).reshape(-1,1)
            y = self.I(get_y,self.data)
            y = y[-self.period:]
            model = LinearRegression().fit(X,y)
            predictions = model.predict(X)
            params = np.append(model.intercept_,model.coef_)
            newX = pd.DataFrame({"Constant":np.ones(len(X))}).join(pd.DataFrame(X))
            MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))
            var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
            sd_b = np.sqrt(var_b)
            ts_b = params/ sd_b
            p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-len(newX.columns)))) for i in ts_b]

            self.p_value[-1] = p_values[1]
            self.coef[-1] = model.coef_
            if (self.coef > 0) and (self.p_value< 0.05):
                #self.close()
                price = self.data.Close[-1]
                self.position.close()
                # self.log('BUY CREATE, %.5f' % self.dataclose[0])
                self.buy(size = 10,tp = price + 0.0006, sl = price - 0.0002)
            if (self.coef < 0) and (self.p_value< 0.05):
                #self.close()
                # self.log('SELL CREATE, %.5f' % self.dataclose[0])
                price = self.data.Close[-1]
                self.position.close()
                self.sell(size = 0.05,tp = price - 0.0006, sl = price + 0.0002)
            if self.p_value > 10:
                self.position.close()

bt = Backtest(eurusd,TestStrategy,cash= 1000)
stats1 = bt.run()