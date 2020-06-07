#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 19:16:41 2020

fieldnames = ["date","Start_time", "End_time", "Activity", "Alternations", "Notes"]

@author: Max
"""
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import csv 
import datetime
import time
import pathlib
import os

import user_interactions

fieldnames = ["Date", "Start_time", "End_time", "Activity", "Alternations", "Notes"]
possible_activities = ['School', "Reading", "Phyton", "CFA", "German"]


def get_last_line(url):
    with open(url, "r") as log:
        x = list(csv.reader(log, delimiter = ","))
        x = np.array(x)
    
        last_line = x[-1,:]
        print(last_line)
        return last_line

def append_new_line(url, new_line):
    with open(url, "a") as log: 
        csv_row = csv.writer(log)
        csv_row.writerow(new_line)
    
def write_new_log(url, fieldnames):
    with open(url, "w") as log: 
        writer = csv.DictWriter(log, fieldnames=fieldnames)
        writer.writeheader()
        return "Log {0} is created\n\n".format(url)

def write_start(start):
    with open("logs/start_time.csv", "w") as starttime_log:
        writer = csv.writer(starttime_log, delimiter = ",")
        writer.writerow(start)    
        
def get_weeknumber():
    weeknumber = datetime.date.today().isocalendar()[1]
    return weeknumber 

def check_if_log_exists(number):
    path = pathlib.Path('logs/log{0}.csv'.format(number))
    return path.exists()

def retrieve_start():
    try: 
        with open("logs/start_time.csv", "r") as start_time:
            x = list(csv.reader(start_time, delimiter = ","))
            os.remove("logs/start_time.csv")
          #  x = np.array(x)
            return x[0]
    except FileNotFoundError:
        return False

def main_function():
    start = retrieve_start()
    current_weeknr = get_weeknumber()
    if not check_if_log_exists(current_weeknr):
        print("\n\nCreating new log \n")
        print(write_new_log("logs/log{0}.csv".format(current_weeknr), fieldnames))
        time.sleep(1)
    if start == False:
        n_activity = user_interactions.get_user_input(possible_activities)
        activity = possible_activities[n_activity]
        start_time = time.strftime('%H:%M:%S', time.localtime())
        write_start([start_time, activity])
        print(" {0} started at {1} \n".format(activity, start_time))
        return
    else:
        print(" Task ended ")
        today = datetime.date.today()
        time_ended = time.localtime()
        time_started = start[0]
        activity = start[1]
        alternation, notes = user_interactions.ask_alternations_notes()
        append_new_line("logs/log{0}.csv".format(current_weeknr), [today, time_started, time_ended, activity, alternation, notes])
        print("Activity logged \n\n")
        return 

#main_function()


           

