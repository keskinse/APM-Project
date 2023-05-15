#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd
import random
data= pd.read_csv("manufacturing.csv")
data.head()


# In[25]:


#selecting relevant rows
selected_rows = data[data['case:cpee:name'] == 'GV12 Keyence MeasuringG']
selected_indices = selected_rows.index.tolist()


# In[26]:


#selecting random indices
num_samples=int(len(selected_indices)* 0.10)
random_indices = random.sample(selected_indices, num_samples)


# In[10]:


for index in random_indices:
    data.loc[index, "data_diameter"] = 60


# In[27]:


data.to_csv('outlier_manufacturing.csv', index=False)

