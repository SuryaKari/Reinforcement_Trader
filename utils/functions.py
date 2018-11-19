import math
import numpy as np


# returns the sigmoid
def sigmoid(x):
    return 1 / (1 + math.exp(-x))




#prints formatted price
def formatPrice(n):
    return ("-$" if n < 0 else "$") + "{0:.2f}".format(abs(n))


    
    
# getState usage res = getState(data['close'].map(float).values,len(data['close']),5)

def getState(data, t, n):
    #data = self.data
    d = t - n + 1
    block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1] # pad with t0
    print('Input State is {}'.format(block))
    return np.array([block])



def decipheraction(action):
    if action == 1:
        val = 'Buy'
    elif action == 2:
        val = 'Sell'
    else:
        val = 'Hold'
    return val