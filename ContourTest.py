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


     
    
def readfile(xlist, ylist,zarray, MZvalues, filename, y_per_x):
    '''
    Takes in the xlist/ylist for testing purposes
    MZvalues represent the m/z values that we want to look for
    filename is the name of the file
    modulation_time represents the 'number of Y values per X value'
    
    This function reads a file line by line until the modulation_time amount is met then begins sorting into defined xlist/ylist
    '''
    counter = 0
    xcounter = 0
    tic_sum = 0
    yholder = []
    p = 0
    for i in range(1, int(y_per_x)+2):
        ylist.append(i)
    
    with open(filename, 'r') as read_obj:
        
        csv_reader = reader(read_obj)  #  read line by line so only one line is in memory at a time
        
        for row in csv_reader:
            if counter > y_per_x:
                zarray.append(yholder)
                xcounter +=1
                xlist.append(xcounter)
                yholder = []
                counter = 0
                p += 1
            for i in MZvalues:
                if row[i] != '':
                    temp = int(row[i])
                tic_sum = tic_sum + temp
            yholder.append(tic_sum)
            tic_sum = 0
            counter += 1
        
    
if __name__ == '__main__':
    
    total_time = 0.0
    start = time.time()    
    
    modulation_time = (2.3)
    acquisitions_persec = 100  # MassSpec sampling rate
    retention_time_1d = ''
    retention_time_2d = ''
    MZvalues = [43, 57, 71, 85, 99]  #  What m/z values you want
    xlist = []
    ylist = []
    zarray = []
    filename = '202200506_DL_1_TertButylOHAc5050_BL_70eVoutput.csv'
    
    #  Can play with these values to determine the right values for out GC run
    #  May need to add the 2.53s to GC runtime
    acquisitions = 389990
    GC_runtimeseconds = 3300
    for i in range(0,len(MZvalues)):
        MZvalues[i] = MZvalues[i] - 30
    y_per_x = modulation_time*acquisitions_persec #  How many y values per x
    
    
    readfile(xlist, ylist, zarray, MZvalues, filename, y_per_x)
    
    end = time.time()
    total_time = end-start
    print(total_time)     
    
    zarray.pop()
    xlist.pop()
    print(len(zarray))
    print(len(zarray[0]))
    print('----')
    print(len(xlist))
    print(len(ylist))
    
    fig,ax=plt.subplots(1,1)
    cp = ax.contourf(ylist, xlist, zarray, levels=[0,150,300,450,600,750,900,1050,1200,1350, 1500], colors=['#0b0bf6', '#8200dc', '#ae00c0', '#cb00a4', '#dd0088', '#e7006e', '#ec0056', '#eb0040', '#e7002c', '#e01217'], extend='both')
    fig.colorbar(cp) # Add a colorbar to a plot
    ax.set_title('Test Contour Plot')
    ax.set_xlabel('Testx')
    ax.set_ylabel('Testy')
    plt.show()
    