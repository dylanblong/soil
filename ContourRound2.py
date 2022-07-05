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


def readfile(xlist, ylist, zarray, MZvalues, filename, y_per_x, solvent_delay, retention1D):
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
    largest = 0

    #  Primes zarray by creating empty containers for every row
    for i in range(0, int(y_per_x)):
        zarray.append([])

    #  Makes ylist with amount of items relevant to number of rows
    for i in range(1, int(y_per_x) + 1):
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
            if tic_sum > largest:
                largest = tic_sum

                #  Appends tic_sum to specific container in zarray that represents the
            #  desired x/y coordinates

            if tic_sum < 100:
                zarray[counter].append(0)

            else:
                zarray[counter].append(np.log10(tic_sum))
            counter += 1  # Moves to the next container
            tic_sum = 0  # Resets the tic_sum for the next row

        #  If we have an incomplete final column, this will remove the last
        #  amount of data at the end of the run as a complete zarray is needed
        #  for matplotlib contour plots to be formed
        if len(zarray[0]) != len(xlist):
            #  If the first row of zarray has an additional item it sets this
            #  amount as the 'max amount' of items allowed in a row
            index = len(zarray[0])
            for i in range(len(zarray)):  # Indexes each row
                #  If the row has an additional item it removes it
                if len(zarray[i]) == index:
                    zarray[i].pop()

        #  Solvent delay work
        xlength = len(xlist)
        slvdelay_slice = int((solvent_delay/retention1D)*xlength)
        print(len(xlist))
        del xlist[:slvdelay_slice]
        print(len(xlist))
        print(slvdelay_slice)
        for i in range(0, y_per_x):
            del zarray[i][:slvdelay_slice]
    return largest


def getTicks(retention_time, scale, solvent_delay):
    '''
    Takes in the retention time and the scale of the desired axis and returns
    a list with desired axis points
    '''

    if retention_time == 2.3:
        ticks = [0]  # 0 is position 0
    else:
        ticks = [solvent_delay]

    value = scale
    while value < ticks[0]:
        value += scale
        print(value)
    #  while the value is less then the retention time each axis increment is added
    while value < retention_time:
        ticks.append(value)
        value += scale
    ticks.append(retention_time)  # append the final value
    print(ticks)
    return ticks  # Returns list of axis values


def getTickPos(listt, ticks, solvent_delay):
    '''
    listt is the respective x/ylist to know how many rows/columns there are in
    the zarray
    ticks is the determined ticks that will be labeled on the x/y axis

    The tick values are taken in and converted to values respective of the array
    index scale so they can be properly labeled on the contour plot
    '''

    tickpos = [0]  # 0 is position 0

    # makes a temp list that can be sliced front/back
    temp = ticks
    temp = temp[1:-1]
    #  Index the temp list to allow for each value to be accounted for
    for i in temp:
        #  Finds the pos by taking the fractional position of each index then
        #  multiplying by the length of the list to get the exact position
        #  for example (10/65) * 1403 = 261 so the position of the 10min
        #  marker will be at index 261 of the array when labeled
        if listt == ylist:
            pos = (i / ticks[-1]) * len(listt)
        else:
            pos = (i-solvent_delay / (ticks[-1])) * len(listt)
            #print('L')
        tickpos.append(pos)
    #  Appends final value of list to the tick position
    tickpos.append(len(listt) - 1)
    return tickpos


def getscale(largest):
    '''
    largest is the value of highest intensity of the respective 2D chromatogram(s)

    returns scale of length 8 which pseudo log scales based on the largest value
    '''
    scale = [1.5]
    count = 0
    item = 1.5
    increment = np.log10(largest)/1200
    while count < 900:
        item = item + increment
        count += 1
        scale.append(item)
    return scale

def fill(min, max):
    '''
    :param min:
    :param max:
    :return:
    '''
    scale_list = []
    increment = (max-min)/200
    current = min
    count = 0
    while count < 201:
        current = current + increment
        scale_list.append(current)
        count += 1
        if current > 50000:
            count += 4
    return scale_list

def getCBticks(scale):
    '''
    :return:
    '''
    max = scale[-1]
    min = scale[0]
    print(min)
    print(max)
    CBticks = []
    for i in range(int(min)+1, int(max)+1):
        item = i
        CBticks.append(item)
    print(CBticks)
    return CBticks


def makeplot(retention_time_1d, retention_time_2d, x_scale, y_scale, largest, solvent_delay):
    '''
    This makes the plot
    '''
    #  Gets the z-axis scale
    scale = getscale(largest)
    #  Makes contour plot by creating subplot, then contour plot with desired
    #  intensity levels and colour scheme (from hexvalues) then adds colourbar
    fig, ax = plt.subplots()
    #cp = plt.contourf(zarray_list[0], levels=scale, locator=[100,1000,10000,100000,1000000], extend='both', cmap='jet')
    cp = plt.contourf(zarray_list[1], levels=scale, locator=([2,3,4]), cmap='jet', extend='both')
    fig.colorbar(cp, label='Intensity') # Add a colorbar to a plot

    #  Set title, xaxis and yaxis labels
    ax.set_title('Test Contour Plot')
    ax.set_xlabel('1D (min)')
    ax.set_ylabel('2D (sec)')

    #  Gets value of ticks based on desired x/y scale
    xticks = getTicks(retention_time_1d, x_scale, solvent_delay)
    yticks = getTicks(retention_time_2d, y_scale, solvent_delay)
    #  Sets ticks at desired x/y positions
    ax.set_xticks(getTickPos(xlist, xticks, solvent_delay))
    ax.set_yticks(getTickPos(ylist, yticks, solvent_delay))
    #  Sets tick labels at previously set positions
    ax.set_xticklabels(xticks, fontdict=None, minor=False)
    ax.set_yticklabels(yticks, fontdict=None, minor=False)
    plt.show()
    return cp


if __name__ == '__main__':

    #  gauge time it takes to make contour plot
    total_time = 0.0
    start = time.time()

    #  Set items here specific to GC run
    modulation_time = 2.3  # in seconds
    acquisitions_persec = 100  # MassSpec sampling rate per second
    retention_time_1d = 65  # retention time of 1D (in minutes)
    x_scale = 10  # value you want x axis to scale by (in minutes)
    retention_time_2d = 2.3  # retention time of 2D  note- value is hard coded in getTicks() and will need to be changed too
    y_scale = 0.5  # value you want the y axis to scale by (in seconds)
    solvent_delay = 11.1  # solvent delay in minutes (change for solvent type)
    MZvalues = [[43, 57, 71, 85, 99], [41, 55, 69, 83, 97]]  # What m/z values you want
    # Alkanes, cycloalkanes
    filename = '202200505_DL_4_EthylAcetate_BL_70eVoutput.csv'
    y_per_x = round(modulation_time * acquisitions_persec)  # How many y values per x
    scaled = 0  # Value the scale is based off of
    zarray_list = []

    #  Shifts MZvalues down 30 to correspond to index they exist in imported csv
    for row in range(0, len(MZvalues)):
        for i in range(0, len(MZvalues[row])):
            MZvalues[row][i] = MZvalues[row][i] - 30
    print(MZvalues)

    #  Loads zarray for each desired m/z value range
    for values in MZvalues:
        #  Container creation and pre-calculations
        xlist = []
        ylist = []
        zarray = []
        print('reset')
        print(zarray)
        #  Call readfile to load the file
        largest = readfile(xlist, ylist, zarray, values, filename, y_per_x, solvent_delay, retention_time_1d)
        #  Appends zarray of respective MZvalue to list
        zarray_list.append(zarray)
        #  If the largest intensity of the MZvalue is larger than the current, it is replaced
        #  so that the largest intensity in all the chromatograms is used to scale
        if largest > scaled:
            scaled = largest

    # Gets
    # fig.colorbar(ax, label='Intensity')  # Add a colorbar to a plot
    makeplot(retention_time_1d, retention_time_2d, x_scale, y_scale, scaled, solvent_delay)
    #  gauge time it takes to make contour plot
    end = time.time()
    total_time = end - start
    print(total_time)

