import pandas as pd
import numpy as np
import pandas_ta as ta
import MetaTrader5 as mt5
from Easy_Trading import Basic_funcs
import pandas_ta as ta


df = pd.DataFrame()

df.ta.indicators()

ta.supertrend()

nombre = 67043467
clave = 'Genttly.2022'
servidor = 'RoboForex-ECN'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

bfs = Basic_funcs(nombre, clave, servidor, path)

rates_frame = bfs.extract_data('USDJPY',mt5.TIMEFRAME_H1,9000)

def iqr_indicator(df,columna,periodo):
    df = df.tail(periodo)
    q1 = df[columna].quantile(0.25)
    q2 = df[columna].quantile(0.75)

    return q1, q2


Q1, Q2 = iqr_indicator(rates_frame,'close',14)

ta.stdev(rates_frame['close'],20)

df = rates_frame[['close','tick_volume']]

df['close'] = round(df['close'],2)

df2 = df.groupby('close')['tick_volume'].sum()


