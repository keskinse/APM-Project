# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 18:42:54 2023

@author: Sergen
"""

import pandas as pd
import pm4py
import re

def preprocess():
    df = pd.read_csv(r'data/BPI_Challenge_2019.csv', encoding='ISO-8859-1')
    df2 = df[['case concept:name','event time:timestamp','event concept:name','case Item','case Spend classification text']].copy()
    for index, row in df2.iterrows():
        full_date = df2.at[index, 'event time:timestamp']
        year = re.findall('\d\d\d\d', full_date)[0]
        two_digits = re.findall('\d\d', full_date)
        
        day = two_digits[0]
        month = two_digits[1]
        hour = two_digits[4]
        minute = two_digits[5]
        second = two_digits[6]
        
        df2.at[index, 'event time:timestamp'] = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        
        if df2.at[index, 'case Spend classification text'] == 'OTHER':
            df2.at[index, 'case Spend classification text'] = 'NPR'
        
    df2.set_index('case concept:name', inplace=True)
    df2.sort_values(by=['case concept:name', 'event time:timestamp'], ascending=True, inplace=True)
    df2.to_csv('data/BPI_preprocessed.csv')

