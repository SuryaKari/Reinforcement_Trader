
# coding: utf-8

# ### Imports

# In[1]:


import numpy as np
import pandas as pd
import math
import sys
sys.path.insert(0,'/root/Rbot/utils')

import data_collection as dc
import time,datetime
from datetime import datetime

from utils import Utils

import functions as f

sys.path.insert(0,'/root/Rbot/agent')
from Agent import Rbot
import pickle


# In[3]:


old_stdout = sys.stdout

log_file = open("/root/Rbot/logs/message.log","w")

sys.stdout = log_file


print("This is the Start of the log")


# ### Initialize Utilitities

# In[3]:


utils = Utils("25 Jun, 2018",["BTCUSDT"])


# ### Update Data
# 
# 
# Run only if you want to update the data for another date or run for another crypto

# In[4]:


data = utils.UpdateDataRbot()


# ### Coding the trading Part

# In[5]:


agent = Rbot(state_size = 10, is_eval = False)


# In[6]:


data = pd.read_pickle('/root/Rbot/data/BTCUSDT.pickle')

data = list(data['Close'].map(float).values)


# ### Hyper Parameter definition

# In[7]:


batch_size = 32
window_size = 9
episode_count = 200
l = len(data) - 1


# ### Trading

# In[8]:


for e in range(episode_count + 1):
    print("Episode " + str(e) + "/" + str(episode_count))
    state = f.getState(data,0,window_size + 1)
    
    total_profit = 0
    
    agent.inventory = []
    
    for t in range(l):
        action = agent.ActRbot(state)
        
        print('****************************')
        print('Action is {}'.format(f.decipheraction(action)))
        
        # hold
        next_state = f.getState(data, t + 1, window_size + 1)
        reward = 0
        
        if action == 1: # buy
            agent.inventory.append(data[t + 1])
            print("Buy: " + f.formatPrice(data[t + 1]))
            print('****************************')

            
        elif action == 2 and len(agent.inventory) > 0: # sell
            bought_price = agent.inventory.pop(0)
            reward = max(data[t + 1] - bought_price, 0)
            total_profit += data[t + 1] - bought_price
            print("Sell: " + f.formatPrice(data[t + 1]) + " | Profit: " + f.formatPrice(data[t + 1] - bought_price))
            print('****************************')

        done = True if t == l - 1 else False
        agent.MemoryRbot(state, action, reward, next_state, done)
        state = next_state

        if done:
            print("--------------------------------")
            print("Total Profit: " + f.formatPrice(total_profit))
            print("--------------------------------")

        if len(agent.memory) > batch_size:
            agent.ReplayRbot(batch_size)

    if e % 1 == 0:
        agent.brain.save("/root/Rbot/models/model_ep" + str(e) + '.h5')
        

