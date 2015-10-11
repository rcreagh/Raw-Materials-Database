# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 10:23:05 2015

@author: rcreagh
"""

import os
import numpy as np
import sqlite3
import pandas as pd

#Change read location to read database
os.chdir("/Users/rcreagh/Documents/Python/Python Class Project")

#Create a connection to database
conn = sqlite3.connect("renewable.db")
cursor = conn.cursor()

#Query location table in database
sql = "SELECT* FROM location;" 

#Query ports table in database
sql2 = "SELECT* FROM ports;"

#Read location table from database using Pandas
df = pd.read_sql(sql, conn)

#Read location table from database using Pandas
df2 = pd.read_sql(sql2, conn)

#Function to calculate distance between 2 points (x1, y1) and (x2, y2)
def distance(x1,y1,x2,y2):
    s = np.sqrt((pow(x2-x1,2)+pow(y2-y1,2)))
    return s

#Function to calculate total transportation cost for each
#raw materials location j
def cost ():
    j = 0
    d = dict()
    
    #Loop that calculates total transportation cost for each possible
    #plant location
    while j < len(df["long"]):
        plant_lat = df["lat"][j]
        plant_long = df["long"][j]
        i = 0        
        k = 0
        cost_to_plant = 0
        total_prod = sum(df["production"])
        newlist = []
        
        #Loop to calculate cost of transporting raw materials from
        #each raw materials location to the location of the plant
        while i < len(df["long"]):
            raw_mat_lat = df["lat"][i]
            raw_mat_long = df["long"][i]
            dist = distance(plant_lat, plant_long, raw_mat_lat, raw_mat_long)
            prod = df["production"][i]
            
            #Cost of transporting raw materials to plant is:
            #Distance between raw materials location 
            #times production amount at raw materials location
            cost_to_plant += dist*prod
            i += 1
        
        #Loop to calculate cost of transporting materials
        #from plant to closest dock
        while k < len(df2["long"]):
            dock_lat = df2["lat"][k]
            dock_long = df2["long"][k]
            dist = distance(plant_lat, plant_long, dock_lat, dock_long)
            #Create list of distance between each dock and the plant            
            newlist.append(dist)
            k += 1
        
        #Total cost of each location is:
        #Cost of transporting raw materials to plant
        #Plus cost of transporting materials from plant to closest dock
        total_cost = min(newlist)*total_prod + cost_to_plant
        
        #Add total cost of each possible location to dictionary        
        d[j] = total_cost
        j += 1
    return d

c = cost()

#Print minimum value in generated list to give location with min cost
print "Location with minimum cost: " + str(min(c, key=lambda k: c[k]))
#Pring lat and long of location with minimum cost
print "Longitude: " + str(df["long"][min(c, key=lambda k: c[k])])
print "Latitude: " + str(df["lat"][min(c, key=lambda k: c[k])])