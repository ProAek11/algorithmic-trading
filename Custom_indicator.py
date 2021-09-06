import pandas as pd
import numpy as np
from talib import RSI
import MetaTrader5 as mt5

name = "your number"
key = "your key"
serv = "Pepperstone-MT5-Live01"
path = r"C:\Program Files\MetaTrader 5 B\terminal64.exe"
symbol = "EURUSD"
lot = 0.02 

# Get the Data
mt5.initialize( login = name, server = serv, password = key, path = path)
        
symbol_info=mt5.symbol_info("EURUSD")
        
rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_H1, 0, 1000)
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

#Create signal

close = np.array(rates_frame['close'])

#Create the RSI indicator
rates_frame['rsi'] = RSI(close, timeperiod = 14)

#Create the Rolling mean
rates_frame['rsi_roll_mean'] = rates_frame['rsi'].rolling(10).mean()

#Create the Rolling std
rates_frame['rsi_roll_std'] = rates_frame['rsi'].rolling(10).std()

#Create the custom signal
rates_frame['custom signal'] = np.where(rates_frame['rsi'] > 2*rates_frame['rsi_roll_std'], 'Sell',
    np.where(rates_frame['rsi'] < 2*rates_frame['rsi_roll_std'], 'Buy', '')
)