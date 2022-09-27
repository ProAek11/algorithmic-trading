import pandas as pd
import numpy as np
import MetaTrader5 as mt5
from Easy_Trading import Basic_funcs
from datetime import datetime
import time



nombre = 67043467
clave = 'Genttly.2022'
servidor = 'RoboForex-ECN'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

bfs = Basic_funcs(nombre,clave,servidor,path)

def extraer_datos(par,periodo,cantidad):
    '''
    Función para extraer los datos de MT5 y convertitlos en un DataFrame

    # Parámetros
    
    - par: Activo a extraer
    - periodo: M1, M5...etc
    - cantidad: Entero con el número de registros a extraer

    '''
    mt5.initialize(login = nombre, password = clave, server = servidor, path = path)
    rates = mt5.copy_rates_from_pos(par, periodo, 0, cantidad)  
    tabla = pd.DataFrame(rates)
    tabla['time']=pd.to_datetime(tabla['time'], unit='s')

    return tabla

df = extraer_datos('EURUSD',mt5.TIMEFRAME_M1,1000)


def calcular_media_movil(tabla,N):
    '''
    '''

    tabla['media_movil'] = tabla['close'].rolling(N).mean()

    return tabla

df2 = calcular_media_movil(df,20)

# def cierre_pos_abiertas():
    
#     array_pos = mt5.positions_get()
#     post = pd.DataFrame(array_pos, columns= array_pos[0]._asdict().keys())

#     lista_tickets = post['ticket'].tolist()

#     for ticket in lista_tickets:
#         temporal = post[post['ticket'] == ticket]
#         deal_id = temporal['ticket'].item()
#         lotaje = temporal['volume'].item()
#         orden_cierre = {"action": mt5.TRADE_ACTION_DEAL,
#                         "symbol": 'EURUSD',
#                         "volume": float(lotaje),
#                         "position": deal_id,
#                         "type": mt5.ORDER_TYPE_SELL,
#                         "magic": 202204,
#                         "comment": "cierre operación",
#                         "type_time": mt5.ORDER_TIME_GTC,
#                         "type_filling": mt5.ORDER_FILLING_FOK

#         }

#         mt5.order_send(orden_cierre)

def abrir_operacion(par,volumen,tipo_operacion):
    orden = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": par,
    "volume": volumen,
    "type": tipo_operacion,
    "magic": 202204,
    "comment": "Bot UdeR1",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_FOK

    }

    mt5.order_send(orden)

    print('Se ejecutó una',tipo_operacion, 'con un volumen de', volumen)

def robotuder1(df2,volumen,par):

    ultimo_ma = df2['media_movil'].iloc[-1]
    penultimo_ma = df2['media_movil'].iloc[-2]

    if ultimo_ma > penultimo_ma:

        abrir_operacion(par,volumen,mt5.ORDER_TYPE_BUY)

    elif ultimo_ma < penultimo_ma:
        
        abrir_operacion(par,volumen,mt5.ORDER_TYPE_SELL)

        
class Robots_URosario():

    def __init__(self,nombre, clave,servidor,path):
        self.nombre = nombre
        self.clave = clave
        self.servidor = servidor
        self.path = path
    
    def extraer_datos(self,par,periodo,cantidad):
        '''
        Función para extraer los datos de MT5 y convertitlos en un DataFrame

        # Parámetros
        
        - par: Activo a extraer
        - periodo: M1, M5...etc
        - cantidad: Entero con el número de registros a extraer

        '''
        mt5.initialize(login = nombre, password = clave, server = servidor, path = path)
        rates = mt5.copy_rates_from_pos(par, periodo, 0, cantidad)  
        tabla = pd.DataFrame(rates)
        tabla['time']=pd.to_datetime(tabla['time'], unit='s')

        return tabla

    def info_account(self):

        '''Desarrollada por Max'''

        mt5.initialize(path=path, login=nombre,password=clave, server=servidor)
        cuentaDict = mt5.account_info()._asdict()
        balance = cuentaDict["balance"]
        profit_account = cuentaDict["profit"]
        equity = cuentaDict["equity"]
        free_margin = cuentaDict["margin_free"]

        return balance, profit_account, equity, free_margin

    def get_all_positions(self):
        '''
        Función auxiliar 2. Sirve para obtener las posiciones abiertas para cada uno de los pares en cada timeframe
        '''
        try:
            #mt5.initialize( login = name, server = serv, password = key, path = path)
            o_pos = mt5.positions_get()
            df_pos = pd.DataFrame (list(o_pos), columns=o_pos[0]._asdict().keys())
            print("Se logró obtener la historia correctamente")
                
        except :
            df_pos = pd.DataFrame()
            print("No se logró obtener la historia correctamente")
        
        return df_pos


    def calcular_media_movil(self,tabla,N):
        '''
        '''

        tabla['media_movil'] = tabla['close'].rolling(N).mean()

        return tabla

    def abrir_operacion(self,par,volumen,tipo_operacion):
        orden = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": par,
        "volume": volumen,
        "type": tipo_operacion,
        "magic": 202204,
        "comment": "Bot UdeR1",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK

        }

        mt5.order_send(orden)

        print('Se ejecutó una',tipo_operacion, 'con un volumen de', volumen)
    
    def robotuder1(self,df2,volumen,par,perc_tp,perc_sl):

        ultimo_ma = df2['media_movil'].iloc[-1]
        penultimo_ma = df2['media_movil'].iloc[-2]

        df_pos = self.get_all_positions()

        if len(df_pos) > 0:
            lista_operaciones = df_pos['ticket'].unique().tolist()
            for ticket in lista_operaciones:
                temp = df_pos[df_pos['ticket'] == ticket]
                profit_actual = temp['profit'].iloc[0]
                balance, profit_account, equity, free_margin = self.info_account()

                if (profit_actual >= equity*perc_tp) or (profit_actual <= equity*perc_sl):
                    bfs.close_all_open_operations()
                
                else:
                    print('No se ha cumplido la condición para cerrar posiciones')

        else:

            print('No existen posiciones abiertas')

        if ultimo_ma > penultimo_ma:

            self.abrir_operacion(par,volumen,mt5.ORDER_TYPE_BUY)

        elif ultimo_ma < penultimo_ma:
            
            self.abrir_operacion(par,volumen,mt5.ORDER_TYPE_SELL)
    
    def handler_robot(self,lista,periodo,cantidad,N,volumen,perc_tp,perc_sl):
        while True:
                        
            for par in lista:
                df = self.extraer_datos(par,periodo,cantidad)
                df2 = self.calcular_media_movil(df,N)
                self.robotuder1(df2,volumen,par,perc_tp,perc_sl)

            time.sleep((60) - datetime.now().second - datetime.now().microsecond/1000000)


ur = Robots_URosario(nombre, clave, servidor, path)

lista = ['EURUSD','GBPAUD','XAUUSD','USDJPY']
ur.handler_robot(lista,mt5.TIMEFRAME_M1,1000,20,0.01,0.002,0.0005)
