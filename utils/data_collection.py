
# coding: utf-8

# In[ ]:


#!pip install python-binance
#!pip install dateparser
import time

import dateparser as dp
from dateutil.parser import parse
import datetime
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

global symbol_list

api_key='etP1gtHy13FYdMEkvwNBPY8KnkeySRdLcH7y8LGpFfp5QV7Ghlvswm54SODy3nWE'
api_secret='JOSKbN1WH0MCTAuVce30CZUHq5psjscRFxYQp10KIXxVAtKE8UYrgPBoPDdJWPWF'

from binance.client import Client
client = Client(api_key, api_secret)


def print_ticker_names(name_str):
    all_symbols=client.get_all_tickers()
    symbols=[]
    for i in range(len(all_symbols)):
        temp=dict((key,value) for key,value in all_symbols[i].items() if key=='symbol')
        temp_list=[]
        temp_list.append(list((value) for (key,value) in temp.items() if key=='symbol'))

        for sublist in temp_list:

            for item in sublist:
                if name_str=='all' or name_str=='ALL':
                    symbols.append(item)

                else:
                    for j in range(len(name_str)):

                        if item[:3]==name_str[j] or item[3:]==name_str[j] or item==name_str[j]:
                            symbols.append(item)
    return(symbols[:10])


def data_collect(symbol_list,start_date,end_date):
    klines=[]
    for i in range(len(symbol_list)):
        temp=[]
        temp=client.get_historical_klines(symbol_list[i], Client.KLINE_INTERVAL_15MINUTE, start_date, end_date)
        klines.append(temp)


    for i in range(len(klines)):
        if i==0:
            df=pd.DataFrame(klines[i])
            df.columns=['Open_time','Open','High','Low','Close','Volume','Close_time','Quote_asset_volume','Number_trades','Taker_Buy_base_asset_Volume','Taker_buy_quote_asset_volume','ignore']
            df['Open_date']=pd.to_datetime(df['Open_time'], unit='ms').dt.date
            df['Close_date']=pd.to_datetime(df['Close_time'], unit='ms').dt.date
            df['Open_time']=pd.to_datetime(df['Open_time'], unit='ms').dt.time
            df['Close_time']=pd.to_datetime(df['Close_time'], unit='ms').dt.time
            df['symbol']=symbol_list[i]
            data_pd=df
            del df
        elif i>0:
            df=pd.DataFrame(klines[i])
            df.columns=['Open_time','Open','High','Low','Close','Volume','Close_time','Quote_asset_volume','Number_trades','Taker_Buy_base_asset_Volume','Taker_buy_quote_asset_volume','ignore']
            df['Open_date']=pd.to_datetime(df['Open_time'], unit='ms').dt.date
            df['Close_date']=pd.to_datetime(df['Close_time'], unit='ms').dt.date
            df['Open_time']=pd.to_datetime(df['Open_time'], unit='ms').dt.time
            df['Close_time']=pd.to_datetime(df['Close_time'], unit='ms').dt.time
            df['symbol']=symbol_list[i]
            data_pd=data_pd.append(df,ignore_index=True)
    del data_pd['ignore']
    del data_pd['Close_time']
    del data_pd['Close_date']
    return(data_pd)

def data_append(data_2018,symbol_list,start_date,end_date):
    klines=[]
    for i in range(len(symbol_list)):
        temp=[]
        temp=client.get_historical_klines(symbol_list[i], Client.KLINE_INTERVAL_15MINUTE, start_date, end_date)
        klines.append(temp)


    for i in range(len(klines)):
        df=pd.DataFrame(klines[i])
        df.columns=['Open_time','Open','High','Low','Close','Volume','Close_time','Quote_asset_volume','Number_trades','Taker_Buy_base_asset_Volume','Taker_buy_quote_asset_volume','ignore']
        df['Open_date']=pd.to_datetime(df['Open_time'], unit='ms').dt.date
        df['Close_date']=pd.to_datetime(df['Close_time'], unit='ms').dt.date
        df['Open_time']=pd.to_datetime(df['Open_time'], unit='ms').dt.time
        df['Close_time']=pd.to_datetime(df['Close_time'], unit='ms').dt.time
        df['symbol']=symbol_list[i]
        del df['ignore']
        del df['Close_time']
        del df['Close_date']
        data_2018=data_2018.append(df,ignore_index=True)
        del df
    return data_2018

