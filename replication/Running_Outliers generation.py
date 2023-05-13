#!/usr/bin/env python
# coding: utf-8

# In[30]:


import pandas as pd
import random


# In[31]:


data= pd.read_csv("running.csv")
data.head()


# In[40]:


#selecting only rows that have measure temperature
selected_rows = data[data['event'] == 'Measure temperature']
selected_indices = selected_rows.index.tolist()


# In[41]:


#selecting random indices
num_samples=int(len(selected_indices)* 0.25)
random_indices = random.sample(selected_indices, num_samples)


# In[42]:


for index in random_indices:
    data.loc[index, "temperature"] = 26
data.head()


# In[43]:


data.to_csv('outlier_running', index=False)

