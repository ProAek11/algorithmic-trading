
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

rates_frame = bfs.extract_data('USDJPY',mt5.TIMEFRAME_H1,9000)
rates_frame['MA_X'] = rates_frame['close'].rolling(50).mean()
rates_frame['diff_meanX'] = rates_frame['close'] - rates_frame['MA_X']

rates_frame['diff_meanX'].plot()
rates_frame['diff_meanX'].hist()

import matplotlib.pyplot as plt



conteo, bins, barras = plt.hist(rates_frame['diff_meanX'])
min_desv = bins[2]
max_desv = bins[-3]

rates_frame['signal'] = np.where(rates_frame['diff_meanX'] >= max_desv,-1,
    np.where(rates_frame['diff_meanX'] <= min_desv,1,0)
 )

rates_frame.to_excel('resultados_ma_reversion.xlsx')

def MR_a_ma(min_desv,max_desv,par):
    while True:
        rates_frame = bfs.extract_data(par,mt5.TIMEFRAME_H1,1000)
        rates_frame['MA_X'] = rates_frame['close'].rolling(50).mean()
        rates_frame['diff_meanX'] = rates_frame['close'] - rates_frame['MA_X']
        ultima_dif = rates_frame['diff_meanX'].iloc[-1]

        if ultima_dif >= max_desv:
            bfs.open_operations(par,0.01,mt5.ORDER_TYPE_SELL)
        elif ultima_dif <= min_desv:
            bfs.open_operations(par,0.01,mt5.ORDER_TYPE_BUY)
        
        else:
            print('No se ha cumplido la condición')

        time.sleep((60) - datetime.now().second - datetime.now().microsecond/1000000)

MR_a_ma(min_desv,max_desv,'USDJPY')
