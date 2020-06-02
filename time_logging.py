#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 19:16:41 2020

fieldnames = ["Start_time", "End_time", "Activity", "Alternations", "Notes"]

@author: Max
"""
import numpy as np
import csv 
from datetime import datetime

import user_interactions

fieldnames = ["Start_time", "End_time", "Activity", "Alternations", "Notes"]

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
        return "Log {0} is created".format(url)

def write_start_time(start_time):
    with open("logs/start_time.csv", "w") as starttime_log:
        writer = csv.writer(starttime_log, delimiter = ",")
        writer.writerow([start_time])
        
