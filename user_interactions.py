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
    for n in range(len(possible_act)):
        print("{0}: for {1}".format(n, possible_act[n]))  
    activity = input("type the number of the activity: ")  
    try:       
       n_activity = int(activity)     
    except:       
        print("\nThat's not a number!, Let's try it again\n")
        activity = ""  
        time.sleep(1)      
        n_activity = get_user_input(possible_act)  
    return n_activity
    
def ask_alternations_notes():
    a = False
    b = False   
    
    while a == False:
        y_n_alt = input("\n Do you want to apply any alternations? Y/N\n").lower()
        if( y_n_alt == "y"):      
            alternation = get_alternation()
            a = True
        elif(y_n_alt == "n"):    
            print("\n No alternations")
            alternation = 0
            a = True 
        else:   
            print("Wrong input")
    
    while b == False:
        y_n_note = input("\n Do you want to add a note? Y/N\n").lower()
        if( y_n_note == "y"):   
            note = input("\n Provide your note:\n")
            b = True
        elif(y_n_note == "n"):  
            print("\n No note")
            note = ""
            b = True    
        else:       
            print("wrong input")
    return alternation, note
        
def get_alternation():
    alternation = input("\n Provide your alternation in minutes:\n")        
    try:         
            n_alternation = int(alternation)        
    except:             
            print("\n That's not a number!, Let's try it again\n")            
            alternation = ""    
            time.sleep(1)        
            n_alternation = get_alternation()        
    return n_alternation

