#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 20:03:19 2020

@author: Max
"""



def calendar_heat_map(week = None):
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
    df['date_revised'] = pd.to_datetime(df["Date"], format='%Y-%m-%d')
    
    df = df.groupby('date_revised').sum()
   
    df.time_delta = df.time_delta / 60
    
    df = df.reset_index()
    
    print(df)
    df['year'] = df['date_revised'].dt.year
    df.set_index('date_revised', inplace=True)


    
    plt.figure(figsize=(16,10), dpi= 80)
    calmap.calendarplot(df['2020']['time_delta'], fig_kws={'figsize': (16,10)}, yearlabel_kws={'color':'black', 'fontsize':14}, subplot_kws={'title':'Time per day'})
    plt.show()
    
            
    return