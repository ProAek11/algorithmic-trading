import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from sklearn.linear_model import LinearRegression
from Easy_Trading import Basic_funcs
from datetime import datetime
import time
from scipy import stats



nombre = 67043467
clave = 'Genttly.2022'
servidor = 'RoboForex-ECN'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

bfs = Basic_funcs(nombre,clave,servidor,path)

def regressor_robot():
    while True:
        rates_frame = bfs.extract_data('EURUSD',mt5.TIMEFRAME_M1,12)
        rates_frame['minutes'] = range(12)
        y = rates_frame['open']
        X = rates_frame[['minutes']]
        model = LinearRegression().fit(X,y)
        rates_frame['predict'] = model.predict(X)

        print(model.coef_)
        params = np.append(model.intercept_,model.coef_)
        predictions = model.predict(X)

        newX = pd.DataFrame({"Constant":np.ones(len(X))}).join(pd.DataFrame(X))
        MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))

        # Note if you don't want to use a DataFrame replace the two lines above with
        # newX = np.append(np.ones((len(X),1)), X, axis=1)
        # MSE = (sum((y-predictions)**2))/(len(newX)-len(newX[0]))

        var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
        sd_b = np.sqrt(var_b)
        ts_b = params/ sd_b

        p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-len(newX.columns)))) for i in ts_b]

        sd_b = np.round(sd_b,3)
        ts_b = np.round(ts_b,3)
        p_values = np.round(p_values,3)

        if model.coef_ > 0 and p_values[1] < 0.05:
            df1 = bfs.get_all_positions()
            len_d_pos = len(df1)
            if len_d_pos > 0 and df1['type'].unique().item() == 1: 
                bfs.close_all_open_operations('EURUSD')
                bfs.open_operations('EURUSD',0.01,mt5.ORDER_TYPE_BUY)
            elif len_d_pos > 0 and df1['type'].unique().item() == 0:
                print('Ya existe una operación de compra abierta')
            else:
                bfs.open_operations('EURUSD',0.01,mt5.ORDER_TYPE_BUY)
            
        elif model.coef_ < 0 and p_values[1] < 0.05:
            df1 = bfs.get_all_positions()
            len_d_pos = len(df1)
            if len_d_pos > 0 and df1['type'].unique().item() == 0: 
                bfs.close_all_open_operations('EURUSD')
                bfs.open_operations('EURUSD',0.01,mt5.ORDER_TYPE_SELL)
            elif len_d_pos > 0 and df1['type'].unique().item() == 1:
                print('Ya existe una operación de venta abierta')
            else:
                bfs.open_operations('EURUSD',0.01,mt5.ORDER_TYPE_SELL)
        else:
            df1 = bfs.get_all_positions()
            len_d_pos = len(df1)
            if len_d_pos > 0 and p_values[1] > 0.05:
                bfs.close_all_open_operations('EURUSD')

        
        time.sleep((60) - datetime.now().second - datetime.now().microsecond/1000000)


regressor_robot()