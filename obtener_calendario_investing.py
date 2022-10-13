from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime
import json
import pandas as pd

def scrapping_investing():
    r = Request('https://es.investing.com/economic-calendar/', headers = {'User-Agent': 'Mozilla/5.0'})

    response = urlopen(r).read()
    soup = BeautifulSoup(response,"html.parser")
    tabla = soup.find_all(class_ = 'js-event-item')

    result = []
    base = {}

    for new in tabla:
        time = new.find(class_ = 'first left time js-time').text
        currency = new.find(class_ = 'left flagCur noWrap').text.split(' ')
        intensity = new.find_all(class_ = 'left textNum sentiment noWrap')

        id_hour = currency[1] + '_' + time

        if not id_hour in base:
            base.update({id_hour:{'currency':currency[1], 'time':time, 'intensity':0}})

            intencity = 0

        for intence in intensity:
            _true = intence.find_all(class_ = 'grayFullBullishIcon')
            if len(_true) == 1:
                intencity = 1
                
            elif len(_true) == 2:
                intencity = 2
                
            elif len(_true) == 3:
                intencity = 3

        base[id_hour].update({'intensity':intencity})

    for b in base:
        result.append(base[b])
        
    return result


noticias = scrapping_investing()

pd.DataFrame.from_records(noticias)
            



