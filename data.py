#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 17:37:15 2020

@author: Max
"""

import pandas as pd 
from datetime import datetime

import time_logging

def minutes_to_hours(minutes):
    hours_float = minutes / 60 
    minutes = int(round(hours_float % 1 * 60))
    hours = int(hours_float - (hours_float%1))
    return "{0}:{1}".format(hours,minutes)
    

def daily_time(wknr = None, day = None):
    # Checks if day is filled, otherwise takes today NEED TO CHECK FOR PANDA COMMAND
    if day == None:
        day = pd.to_datetime(datetime.today().date(),format='%Y-%m-%d')
        wknr = time_logging.get_weeknumber()
    else:
        day = pd.to_datetime(datetime.strptime(day,'%Y-%m-%d').date())
    #Read out csv to dataframe
    df = pd.read_csv('logs/log{0}.csv'.format(wknr))       
    #edit date column to date format
    df['date_revised'] = pd.to_datetime(df["Date"], format='%Y-%m-%d')
    #created daily dataframe
    
    df.Start_time = pd.to_datetime(df['Start_time'])
    df.End_time = pd.to_datetime(df['End_time'])
    df['time_delta'] = df.apply(lambda row: pd.Timedelta(row['End_time'] - row['Start_time']).seconds / 60 + row['Alternations'], axis = 1)
   
    df_day = df[df.date_revised == day]
    total_day = df_day.time_delta.sum()
    
    return minutes_to_hours(total_day) 

def weekly_avg(weeknr = None):
    if weeknr == None:
        weeknr = time_logging.get_weeknumber()
    try:
        df = pd.read_csv('logs/log{0}.csv'.format(weeknr))
    except:  
        return 'weeknumber not available'
    
    df.Start_time = pd.to_datetime(df['Start_time'])
    df.End_time = pd.to_datetime(df['End_time'])
    
    df['time_delta'] = df.apply(lambda row: pd.Timedelta(row['End_time'] - row['Start_time']).seconds / 60 + row['Alternations'], axis = 1)
    
    n_days = df.Date.nunique()
    total_hours = df.time_delta.sum()
    avg_daily = total_hours / n_days 
    return minutes_to_hours(avg_daily)

if __name__ == '__main__':
    a = False
    b = False 
    
    input_data = input("Do you wat weekly average or daily stats? W/D\n").lower()
    
    if input_data == 'w':
        while a == False:
            weeknumber = input("\n Stats for which week? if current week, use c").lower()
            if weeknumber == 'c':
                print(weekly_avg())
                a = True
            else:
                try:
                    n_wknr = int(weeknumber)
                    print(weekly_avg(n_wknr))
                    a = True 
                except:
                    print("that is not a number")
    if input_data == 'd':
        while a == False:
            day = input("\n Stats for which day (Y-M-D)? if current day, use c").lower()
            if day == 'c':
                print(daily_time())
                a = True
            else:
                try:
                    wknr = time_logging.get_weeknumber(day)
                    print(daily_time(wknr, day))
                    a = True 
                except:
                    print("that is not a date")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


