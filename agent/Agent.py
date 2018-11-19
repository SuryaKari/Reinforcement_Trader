
# coding: utf-8

# In[8]:


import keras
from keras.layers.core import Dense, Activation
from keras.models import load_model
from keras.optimizers import Adam
from keras.models import Sequential

import numpy as np
import pandas as pd
from collections import deque
import random



# In[1]:


class Rbot(): #Agent Code : Torobot007
    
    def __init__(self,state_size,is_eval = False):
        
        # Declare the Agent Hyper-parameters
        
        self.learning_rate = 0.01
        self.is_eval = is_eval
        self.inventory = []
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.gamma = 0.8
        self.state_size = state_size
        self.action_size = 3 # Hold,Buy,Sell
        self.memory = deque(maxlen = 1000)
        self.model_name = 'Rbot.h5'
        #self.brain = self.BuildRbot()
        self.brain = load_model("models/" + self.model_name) if is_eval else self.BuildRbot()
        
        
    # Brain Module of Rbot
        
    def BuildRbot(self):
        
        # Start with a simple MLP
        
        model = Sequential()
        model.add(Dense(units=64, input_dim=self.state_size, activation="relu"))
        model.add(Dense(units=32, activation="relu"))
        model.add(Dense(units=8, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))
        
        return model 

    
    # Memory Module of Rbot
    
    def MemoryRbot(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))
        
    
    # Action Module of Rbot
    
    def ActRbot(self,state):
        if self.is_eval and np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        action = self.brain.predict(state)
        return np.argmax(action[0])
    
    
    # Replay Module of Rbot
    
    def ReplayRbot(self,batch_size):
        sample = random.sample(self.memory,batch_size)
        for state,action,reward,next_state,done in sample:
            target = reward # if done == True
            if not done:
                target = reward + self.gamma * np.argmax(self.brain.predict(next_state)[0])
            target_f = self.brain.predict(state)
            target_f[0][action] = target
            self.brain.fit(state,target_f,epochs = 1,verbose = 0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

