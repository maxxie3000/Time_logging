#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 19:16:42 2020

handles user inputs and outputs

@author: Max
"""

import time

def get_user_input(possible_act):
    print("What activity are you going to do? ")
    for n in possible_act:
        print("{0}: for {1}".format(n, possible_act[n-1]))
    activity = input("type the number of the activity: ")
    try: 
        n_activity = int(activity)
    except: 
        print("\nThat's not a number!, Let's try it again\n")
        activity = ""
        time.sleep(1)
        get_user_input(possible_act)
    return possible_act[n_activity-1]
    

