#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 17:37:15 2020

@author: Max
"""

import pandas as pd 
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
from os import listdir
import calmap

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

def running_weekly_avg(date = None):
    wknr = time_logging.get_weeknumber(date)
    df_1 = pd.read_csv("logs/log{0}.csv".format(wknr-1))
    df_2 = pd.read_csv("logs/log{0}.csv".format(wknr))
    if date == None:
        daynr = pd.to_datetime(datetime.today().date(),format='%Y-%m-%d').weekday()
    else:
        daynr = pd.to_datetime(datetime.strptime(date,'%Y-%m-%d').date()).weekday()
    df_1['date_revised'] = pd.to_datetime(df_1["Date"], format='%Y-%m-%d')
    df_2['date_revised'] = pd.to_datetime(df_2["Date"], format='%Y-%m-%d')
    df_1['weekday'] = df_1['date_revised'].dt.weekday
    df_2['weekday'] = df_2['date_revised'].dt.weekday
    
    df_1 = df_1[df_1['weekday'] >= daynr]
    
    df_1.Start_time = pd.to_datetime(df_1['Start_time'])
    df_1.End_time = pd.to_datetime(df_1['End_time'])
    df_2.Start_time = pd.to_datetime(df_2['Start_time'])
    df_2.End_time = pd.to_datetime(df_2['End_time'])
    
    df_1['time_delta'] = df_1.apply(lambda row: pd.Timedelta(row['End_time'] - row['Start_time']).seconds / 60 + row['Alternations'], axis = 1)
    df_2['time_delta'] = df_2.apply(lambda row: pd.Timedelta(row['End_time'] - row['Start_time']).seconds / 60 + row['Alternations'], axis = 1)
    
    df_1 = df_1.groupby(['Date']).sum()
    df_1.time_delta = df_1.time_delta / 60 
    
    df_2 = df_2.groupby(['Date']).sum()
    df_2.time_delta = df_2.time_delta / 60 
    
    df_1 = df_1.append(df_2)
    
    df_1 = df_1.reset_index()
   

    c = ['red', 'slateblue', 'midnightblue', 'darkslategrey', 'sandybrown', 'palevioletred', 'orange']

    
    plt.figure( figsize=(16,10), dpi=80)
    plt.bar(df_1['Date'], df_1['time_delta'], color = c, width=.8)
    for i, val in enumerate(df_1['time_delta'].values.round(2)):
       plt.text(i, val, float(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight':500, 'size':22})  
    
    plt.gca().set_xticklabels(df_1['Date'], rotation=60, horizontalalignment= 'right', fontdict={'fontweight':500, 'size':22})
    plt.title("Time per day", fontsize=22)
    plt.ylabel('Hours')
    plt.ylim(0, 10)
    plt.yticks(fontsize=22)
    plt.show()
    return

def find_files(path, suffix = '.csv'):
    filenames = listdir(path)
    files = []
    for file in filenames:
        if file.endswith(suffix):
            files.append(file)
    try:
        files.remove('start_time.csv')
    except:
        print('No start_time file')
    return files
        
def stacked_lines(week = None):
    mycolors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:brown', 'tab:grey', 'tab:pink', 'tab:olive']  
    if week == None:
        files = find_files("logs/")
    else:
        try:
            files = "log{0}.csv".format(week)
        except:
            print("Week not available")
            
    df = pd.DataFrame()
    for file in files:
        df = df.append(pd.read_csv("logs/{0}".format(file)))
        
    
    df.Start_time = pd.to_datetime(df['Start_time'])
    df.End_time = pd.to_datetime(df['End_time'])
    
    df['time_delta'] = df.apply(lambda row: pd.Timedelta(row['End_time'] - row['Start_time']).seconds / 60 + row['Alternations'], axis = 1)
    df = df.drop('Alternations', axis = 1)
    
    df.time_delta = df.time_delta / 60
    
    df['date_revised'] = pd.to_datetime(df["Date"], format='%Y-%m-%d')


    df_1 = df.date_revised.unique()
    
    df_2 = df.Activity.unique()
    
    df = df.groupby(['date_revised', 'Activity']).sum()    
    
    df = df.reset_index()

    data = {}

    for index,row in df.iterrows():
        print(row)
        if row['date_revised'] in data:
             
            index = time_logging.possible_activities.index(row['Activity'])
     
            
            data[row['date_revised']][index] += row['time_delta']
          
            
             
        else:
            
            data[row['date_revised']] = [0] * len(time_logging.possible_activities)
            print(data[row['date_revised']])
            index = time_logging.possible_activities.index(row['Activity'])
            data[row['date_revised']][index] += row['time_delta']
    
    df_1 = pd.DataFrame(data)
    df_1 = df_1.transpose()       
            
    
    #y = df[columns[0]].values.tolist()
    print(df_1)
    
    
    #fig, ax = plt.subplots(1,1,figsize=(16, 9), dpi= 80)
    #columns = df.columns[1:]
    #labs = columns.values.tolist()
    
    

stacked_lines()

"""
if __name__ == '__main__':
    a = False
    b = False 
    
    input_data = input("Do you wat weekly average or daily stats? W/D\n").lower()
    
    if input_data == 'w':
        while a == False:
            weeknumber = input("\n Stats for which week? if current week, use c\n").lower()
            if weeknumber == 'c':
                print(weekly_avg())
                running_weekly_avg()
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
                    
                    """