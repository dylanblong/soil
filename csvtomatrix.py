# This is a sample Python script.
from csv import reader
import csv
import time


def csvreadline(file, outputfilename):
    '''
    Reads the imported csv line by line and groups them into bactches of 3 rows
    The batches of 3 rows are then called with sort() to sort them into the finalized array
    '''
    
    rows = 0
    triplerow = []

    #  Opens the csv file in read mode
    with open(file, 'r') as read_obj:
        csv_reader = reader(read_obj)  #  read line by line so only one line is in emmory at a time
        header = next(csv_reader)  # skips the header row at the top of the csv
        if header != None:
            for i in range(1):  # can be used to test larger scale csvs, can be deleted later
                for row in csv_reader:
                    triplerow.append(row)  # appends row in memory to 'triple row'
                    rows += 1
                    if rows == 3:  #  if three rows are in it calls sort() and resets the triplerow container and row counter
                        sort(triplerow, outputfilename)
                        triplerow = []
                        rows = 0
                        
def sort(rows, outputfilename):
    '''
    This sorts the recieved 'triple row' into its repsective spot in the sorted array list
    For example sorted[10][42] represents the 11th aquisition at the (42+30) 72 m/z
    '''
    sorted_row = [0]*1200  #  makes the empty list of 0s for array
    count = 0
    row1 = rows[0]
    for item in rows[0]:
        if count > 1:
            if item != '':
                
                #print(item)
                position = round(float(item)) - 30
                index = row1.index(item)
                #print(position)
                value = rows[1][index] 
                #print(value)
                sorted_row[position] = value
        count += 1
    writeline(sorted_row, outputfilename)
    #final_array.append(sorted_row)
    #print(sorted_row)
    
        
def writeline(sorted_row, outputfilename):
    with open(outputfilename, 'a', newline= '') as f:
        writer = csv.writer(f)
        writer.writerow(sorted_row)
    

    

if __name__ == '__main__':
    total_time = 0.0
    #start = time.time()
    #inputfilename = 'ff'
    #with open('queue.txt', 'r') as file:
        #while inputfilename != '':
            #inputfilename = file.readline()
            #inputfilename = inputfilename[:-1]

            #outputfilename = inputfilename[:-4]
            #outputfilename = outputfilename + 'output.csv'
            #if inputfilename != '':
                #print('currently working on ' + inputfilename + ' into ' + outputfilename)
                #csvreadline(inputfilename, outputfilename)

        #print('hi')




    inputfilename = '20220706_SAS_EYM_ISwithNapoli_1_750688_70eV.csv'
    outputfilename = '20220706_SAS_EYM_ISwithNapoli_1_750688_70eVoutput.csv'

    csvreadline(inputfilename, outputfilename)
    #writeline(final_array, outputfilename)
    
    end = time.time()
    total_time = start-end
    print(total_time)    
    
