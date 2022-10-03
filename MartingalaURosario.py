import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from sklearn.linear_model import LinearRegression #Librería para realizar la Rgresión
from Easy_Trading import Basic_funcs
from datetime import datetime
import time
from scipy import stats # Calcular los p-valores

nombre = 67043467
clave = 'Genttly.2022'
servidor = 'RoboForex-ECN'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

bfs = Basic_funcs(nombre, clave, servidor, path)

def martingalaUR():
    while True:
        rates_frame = bfs.extract_data('BTCUSD',mt5.TIMEFRAME_H4,1000)
        rates_frame['MA_X'] = rates_frame['close'].rolling(200).mean()

        ultima_ma = rates_frame['MA_X'].iloc[-1]
        ultimo_close = rates_frame['close'].iloc[-1]

        if ultimo_close < ultima_ma:
            df1 = bfs.get_all_positions()
            len_d_pos = len(df1)

            if len_d_pos > 0:
                profit_acum = df1['profit'].sum()
                if profit_acum < 0:
                    bfs.open_operations('BTCUSD',0.01*2*len_d_pos,mt5.ORDER_TYPE_BUY)
                else:
                    bfs.close_all_open_operations('BTCUSD')
            else:
                bfs.open_operations('BTCUSD',0.01,mt5.ORDER_TYPE_BUY)
        
        time.sleep((60) - datetime.now().second - datetime.now().microsecond/1000000)


martingalaUR()     