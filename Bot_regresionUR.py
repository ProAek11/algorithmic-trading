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

def regressor_robotUR():
    while True:
        ######################## Extracción ######################## 
        rates_frame = bfs.extract_data('XAUUSD',mt5.TIMEFRAME_M1,15)
        ######################## Transformación ######################## 
        y = rates_frame[['close']]
        rates_frame['minutos'] = range(15)
        X = rates_frame[["minutos"]]
        ######################## Crear la Señal ########################

        modelo = LinearRegression().fit(X,y)

        ####################### Hallas la pendiente ####################

        senal = modelo.coef_

        params = np.append(model.intercept_,model.coef_)
        predictions = model.predict(X)

        newX = pd.DataFrame({"Constant":np.ones(len(X))}).join(pd.DataFrame(X))
        MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))
        var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
        sd_b = np.sqrt(var_b)
        ts_b = params/ sd_b

        p_values =[2*(1-stats.t.cdf(np.abs(i),(len(newX)-len(newX.columns)))) for i in ts_b]

        sd_b = np.round(sd_b,3)
        ts_b = np.round(ts_b,3)
        p_values = np.round(p_values,3)

        p_values[1]

        if senal > 0:
            #Cerrar todas las posiciones en venta
            df1 = bfs.get_all_positions()
            len_d_pos = len(df1)

            if len_d_pos > 0 and df1['type'].unique().item() == 1:
                bfs.close_all_open_operations('XAUUSD')
                bfs.open_operations('XAUUSD',0.01,mt5.ORDER_TYPE_BUY)
            elif len_d_pos > 0 and df1['type'].unique().item() == 0:
                print('Ya hay una compra')
            else:
                bfs.open_operations('XAUUSD',0.01,mt5.ORDER_TYPE_BUY)
   

        if senal < 0:
            df1 = bfs.get_all_positions()
            len_d_pos = len(df1)

            if len_d_pos > 0 and df1['type'].unique().item() == 0:
                bfs.close_all_open_operations('XAUUSD')
                bfs.open_operations('XAUUSD',0.01,mt5.ORDER_TYPE_SELL)
            elif len_d_pos > 0 and df1['type'].unique().item() == 1:
                print('Ya hay una venta')
            else:
                bfs.open_operations('XAUUSD',0.01,mt5.ORDER_TYPE_SELL)
            #Cerrar todas las posiciones en compra
            #Condición para solo abrir una operación
        
        time.sleep((60) - datetime.now().second - datetime.now().microsecond/1000000)


regressor_robotUR()
