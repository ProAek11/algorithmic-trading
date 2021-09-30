import pandas as pd
import numpy as np
import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta
import os
print(os.getcwd())
import MetaTrader5 as mt5
import time
from time import sleep
from subprocess import call
import matplotlib.pyplot as plt
import pandasql as ps
import talib
from talib import RSI, EMA


name = 111111111111
key = "xxxxxxxxx"
serv = "xxxxxxxx"
path = r"C:\Program Files\MetaTrader 5\terminal64.exe"
symbol = "EURUSD"
lot = 0.5

mt5.initialize( login = name, server = serv, password = key, path = path)
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 100)
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
rates_frame['variation'] = rates_frame['close'] - rates_frame['open']

variations = rates_frame['variation']
close = rates_frame['close']

l_var = variations[99]
l_close = close[99]
deviation = 1
price = mt5.symbol_info_tick(symbol).ask
range1 = 10

#If there is no positions we will use a var = 0. If there is positions we 
#will use var != 0. var will be the x times we will increment the volume of the next operation

try:
    o_pos = mt5.positions_get()
    df_pos = pd.DataFrame (list(o_pos), columns=o_pos[0]._asdict().keys())
    var = len(df_pos)

except:
    var = 0

# Every time we run de code one long position will be opened
if  l_var >0:
    request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "tp": price + range1,
                "deviation": deviation,
                "magic": 202101,
                "comment": "This is a test",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK}
    mt5.order_send(request)

# if there is no open position we will open one aditional operation

if var == 0 and l_var >0:
    request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "tp": price + range1,
                "deviation": deviation,
                "magic": 202101,
                "comment": "This is a test",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK}
    mt5.order_send(request)

# if there is at least one open position, we will open the opposite order with var times the initial volume
if var >0 and l_var >0:
    request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot*var,
                "type": mt5.ORDER_TYPE_SELL,
                "tp": price - range1,
                "deviation": deviation,
                "magic": 202101,
                "comment": "This is a test",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK}
    mt5.order_send(request)