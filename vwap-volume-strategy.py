#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf
import numpy as np
import pandas as pd

#download the data
df = yf.download('SPY',interval='5m',period='60d')

#flatten multi level columns(eg:('Close','SPY')->'Close')
df.columns = [col[0] if isinstance(col,tuple) else col for col in df.columns]

#calculate vwap
df['cum-vol-price'] = (df['Volume']*df['Close']).cumsum()
df['cum-vol'] = df['Volume'].cumsum()
df['VWAP'] = df['cum-vol-price']/df['cum-vol']

#generate signals
df['signal'] = np.where(
    (df['Close']>df['VWAP'])&
    (df['Volume']>df['Volume'].rolling(10).mean()),1,0)

#strategy backtest
df['Returns'] = df['Close'].pct_change()
df['Strategy_Return'] = df['signal'].shift(1)*df['Returns']

#summerize performance

strat_return = (df['Strategy_Return'] + 1).prod() - 1
bh_return = (df['Returns'] + 1).prod() - 1

print(f"Strategy Return: {strat_return:.2%}")
print(f"Buy & Hold Return: {bh_return:.2%}")




# In[ ]:




