# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 10:23:05 2015

@author: rcreagh
"""

import os
import sqlite3
import numpy as np
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