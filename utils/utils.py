
# coding: utf-8

# In[277]:


import numpy as np
import pandas as pd
import math
import data_collection as dc
import time,datetime
from datetime import datetime


class Utils():
    
    def __init__(self,startdate,symbol):
        self.startdate = startdate
        self.data = np.nan
        self.symbol = symbol
        # self.t = t
        # self.n = n
        
    def UpdateDataRbot(self):
        
        # Date Format : "1 Oct, 2017"
        # Symbol examples : ["BTCUSDT"] or multiple ["ETCUSDT", "BCCUSDT"]
        
        data_2018=dc.data_collect(self.symbol,self.startdate,str(int(time.mktime(datetime.now().timetuple()))))
        data_2018.to_pickle('/root/Rbot/data/{}.pickle'.format(self.symbol[0].replace("'",'')))
        data_2018.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'},     inplace=True)
        data_2018_list = list(data_2018['close'])
        data_2018_list_float = [np.float(x) for x in data_2018_list]
        self.data = data_2018_list_float
        #self.data = data_2018
        
            
        
        return self.data