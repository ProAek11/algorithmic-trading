# Asignación de Variables

variable_1 = 12
variable_2 = '35'
variable_3 = 23.5
variable_4 = True

type(variable_4)

variable_5 = variable_1 - variable_3
variable_6 = variable_1 + variable_3
variable_7 = variable_1 * variable_3
variable_8 = variable_1 / variable_3

variable_9 = float(variable_2) + 1

lista_1 = [variable_1,variable_2,variable_3]

print(lista_1)

print(lista_1[0])
print(lista_1[1])
print(lista_1[2])

lista_1[0] = 54

for i in lista_1:
    print(i,type(i))

lista_nueva = [1,2,3]

lista_1[0] = lista_nueva[0]
lista_1[1] = lista_nueva[1]

# len(lista_1)
# range(3)

for n in range(len(lista_1)):
    lista_1[n] = lista_nueva[n]

print(lista_1)

if variable_1 == 10:
    print(variable_1 + 2)
elif (variable_1 >= 12) or (variable_2 == '34'):
    print('La variable si es mayor a 12')
else:
    print('La variable 1 no es igual a 10')

def multiplicar(var1,var2):
   print(var1*var2)

def dividir(var1,var2):
   print(var1/var2)

def calculadora(var1,var2,operacion):
    if operacion == 'mult':
        multiplicar(var1,var2)
    if operacion == 'div':
        dividir(var1,var2) 


from socket import CAN_RAW
import MetaTrader5 as mt5

nombre = 67043467
clave = 'Genttly.2022'
servidor = 'RoboForex-ECN'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'

mt5.initialize(login = nombre, password = clave, server = servidor, path = path)

un_dict = {'precio':0.9983,'fecha':'2022-09-18','simbolo':'EURUSD'}

un_dict['precio'] = 0.

import pandas as pd

df1 = pd.DataFrame([un_dict])

rates = mt5.copy_rates_from_pos('BRENT', mt5.TIMEFRAME_M1, 0, 2000)  
tabla = pd.DataFrame(rates)

tabla['open'].iloc[0]
tabla.iloc[0,0]

tabla['open'] - tabla['close']

tabla['open'].sum()
tabla['open'].mean()
tabla['open'].rolling(10).mean()

tabla['time'] = pd.to_datetime(tabla['time'],unit='s')


class Carros():

    def __init__(self,cilindraje,peso,color,marca):
        self.color = color
        self.peso = peso
        self.cilindraje = cilindraje
        self.marca = marca
        
    def encender_auto(self):
        print('El auto de marca',self.marca, 'está encendido')


color = 'Azul'
peso = 35
cilindraje = 2000
marca = 'Chevrolet GT'

el_carro_de_dany = Carros(color,peso,cilindraje,marca)
el_carro_de_dany.encender_auto()

orden = {
    "action": mt5.TRADE_ACTION_DEAL,
 "symbol": 'EURUSD',
 "volume": 0.01,
 "type": mt5.ORDER_TYPE_BUY,
 "magic": 202204,
 "comment": "My Bot",
 "type_time": mt5.ORDER_TIME_GTC,
 "type_filling": mt5.ORDER_FILLING_FOK

}

mt5.order_send(orden)

for i in range(50):
   mt5.order_send(orden)

array_pos = mt5.positions_get()
post = pd.DataFrame(array_pos, columns= array_pos[0]._asdict().keys())

lista_tickets = post['ticket'].tolist()

for ticket in lista_tickets:
    temporal = post[post['ticket'] == ticket]
    deal_id = temporal['ticket'].item()
    lotaje = temporal['volume'].item()
    orden_cierre = {"action": mt5.TRADE_ACTION_DEAL,
                    "symbol": 'EURUSD',
                    "volume": float(lotaje),
                    "position": deal_id,
                    "type": mt5.ORDER_TYPE_SELL,
                    "magic": 202204,
                    "comment": "cierre operación",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_FOK

    }

    mt5.order_send(orden_cierre)


###################################################################################
# Análisis de igualdad #

data = pd.read_excel('resultados_pruebas.xlsx')

from scipy.stats import ttest_rel

stat, p = ttest_rel(data['Backtesting'], data['Demo'])

if p > 0.05:
    print("Las dos muestras son estadísticamente iguales con un nivel de confianza de", 1-0.05)
else:
    print("Las dos muestras son estadísticamente diferentes con un nivel de confianza de",  1-0.05)


stat, p = ttest_rel(data['Backtesting'], data['real'])

if p > 0.05:
    print("Las dos muestras son estadísticamente iguales con un nivel de confianza de", 1-0.05)
else:
    print("Las dos muestras son estadísticamente diferentes con un nivel de confianza de",  1-0.05)