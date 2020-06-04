#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 17:37:15 2020

@author: Max
"""

import pandas as pd 
from datetime import datetime

def daily_time(log, day = None):
    # Checks if day is filled, otherwise takes today NEED TO CHECK FOR PANDA COMMAND
    if day == None:
        day = pd.to_datetime(datetime.today().date(),format='%Y-%m-%d')
    else:
        day = pd.to_datetime(datetime.strptime(day,'%Y-%m-%d').date())
    #Read out csv to dataframe
    df = pd.read_csv(log)       
    #edit date column to date format
    df['date_revised'] = pd.to_datetime(df["Date"], format='%Y-%m-%d')
    #created daily dataframe
    df_day = df[df.date_revised == day]
   
    return df_day

print(daily_time("logs/log1.csv"))
