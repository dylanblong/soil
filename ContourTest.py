# This is my contour testing stuff

#   INFO I MAY NEED
# Modulation time 2.3s + 0.23s flush
# 55 min run = 3300s
#  1tba 1048524 lines
#  1hex 1048574     this is excels limit

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from csv import reader
import csv
import time


     
    
def readfile(xlist, ylist, zarray, MZvalues, filename, y_per_x):
    '''
    xlist is container for the x dimension- How many columns?
    ylist is container for the y dimension- How many rows?
    zarray is container that contains intensities at certain x/y coordinate
    MZvalues represent the m/z values that we want to look for
    filename is the name of the file
    y_per_x represents the number of acquisions per modulation
    
    This function reads a file line by line and appends to zarray everytime the
    y_per_x acqusion count is met, representing a new column in the data
    '''
    counter = 0
    tic_sum = 0
    xcounter = 1
    
    #  Primes zarray by creating empty containers for every row
    for i in range(0, int(y_per_x)):
        zarray.append([])
        
    #  Makes ylist with amount of items relevant to number of rows
    for i in range(1, int(y_per_x)+1):
        ylist.append(i)    
            
    #  Opens file in readmode       
    with open(filename, 'r') as read_obj:       
        #  read line by line so only one line is in memory at a time    
        csv_reader = reader(read_obj)  
        
        #  Loads a row from csv_reader one at a time
        for row in csv_reader:
            #  If the counter == y_per_x we know that one modulation of the 2D has occured
            if counter == y_per_x:
                #  setting the counter to 0 allows us to append to the first item
                #  in zarray again allowing us to index zarray as we load rows until
                #  we reach y_per_x again
                counter = 0  
                xlist.append(xcounter)  # Appends value to xlist to represent a new column
                xcounter += 1
                
            #  Checks intensity of each m/z value and adds together
            for i in MZvalues:
                if row[i] != '':
                    temp = int(row[i])
                tic_sum = tic_sum + temp  
            
            #  Appends tic_sum to specific container in zarray that represents the
            #  desired x/y coordinates
            zarray[counter].append(tic_sum)
            counter += 1 #  Moves to the next container
            tic_sum = 0 #  Resets the tic_sum for the next row
            
        #  If we have an incomplete final column, this will remove the last
        #  amount of data at the end of the run as a complete zarray is needed 
        #  for matplotlib contour plots to be formed
        if len(zarray[0]) != len(xlist): 
            #  If the first row of zarray has an additional item it sets this 
            #  amount as the 'max amount' of items allowed in a row
            index = len(zarray[0])
            for i in range(len(zarray)):  #  Indexes each row
                #  If the row has an additional item it removes it
                if len(zarray[i]) == index:  
                    zarray[i].pop()
    
if __name__ == '__main__':
    
    #  guage time it takes to make contour plot
    total_time = 0.0
    start = time.time()    
    
    #  Set items here specific to GC run
    modulation_time = 2.3  #  in seconds
    acquisitions_persec = 100  # MassSpec sampling rate per second
    retention_time_1d = ''  # retention time of 1D
    retention_time_2d = ''  # retention time of 2D
    MZvalues = [43, 57, 71, 85, 99]  #  What m/z values you want
    filename = '202200506_DL_1_TertButylOHAc5050_BL_70eVoutput.csv'
    
    #  Container creation and pre-calculations
    y_per_x = round(modulation_time*acquisitions_persec) #  How many y values per x
    xlist = []
    ylist = []
    zarray = []    
    #  Shifts MZvalues down 30 to correspond to index they exist in imported csv
    for i in range(0,len(MZvalues)):
        MZvalues[i] = MZvalues[i] - 30
        
    
    
    
    #  Call readfile to load the file
    readfile(xlist, ylist, zarray, MZvalues, filename, y_per_x)
    
    
    fig,ax=plt.subplots(1,1)
    cp = ax.contourf(xlist, ylist, zarray, levels=[0,150,300,450,600,750,900,1050,1200,1350, 1500], colors=['#0b0bf6', '#8200dc', '#ae00c0', '#cb00a4', '#dd0088', '#e7006e', '#ec0056', '#eb0040', '#e7002c', '#e01217'], extend='both')
    fig.colorbar(cp) # Add a colorbar to a plot
    ax.set_title('Test Contour Plot')
    ax.set_xlabel('Testx')
    ax.set_ylabel('Testy')
    plt.show()
    
    #  guage time it takes to make contour plot
    end = time.time()
    total_time = end-start
    print(total_time)       