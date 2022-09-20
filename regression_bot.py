import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from sklearn.linear_model import LinearRegression

nombre = 67043467
clave = 'Genttly.2022'
servidor = 'RoboForex-ECN'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

# Get the Data
mt5.initialize( login = nombre, server = servidor, password = clave, path = path)
        
symbol_info=mt5.symbol_info("EURUSD")
        
rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_D1, 0, 10)
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

rates_frame['minutes'] = rates_frame['time'].dt.minute
y = rates_frame['open']
X = rates_frame[['minutes']]
model = LinearRegression().fit(X,y)
rates_frame['predict'] = model.predict(X)

print(model.coef_)

rates_frame['open'].plot()
rates_frame['predict'].plot()