#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 17:37:15 2020

@author: Max
"""

import pandas as pd 
from datetime import datetime

import time_logging

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
    
    df.Start_time = pd.to_datetime(df['Start_time'])
    df.End_time = pd.to_datetime(df['End_time'])
    df['time_delta'] = df.apply(lambda row: pd.Timedelta(row['End_time'] - row['Start_time']).seconds / 60 + row['Alternations'], axis = 1)
   
    df_day = df[df.date_revised == day]
    total_day = df_day.time_delta.sum() / 60 
    minutes = int(round(total_day % 1 * 60))
    hours = int(total_day - (total_day%1))
    print(df_day)
    total = "{0}:{1}".format(hours,minutes)
    return total 

def weekly_avg(weeknr = None):
    if weeknr == None:
        weeknr = time_logging.get_weeknumber()
    df = pd.read_csv('logs/log{0}.csv'.format(weeknr))
    n_days = df.Date.nunique()
    return n_days


