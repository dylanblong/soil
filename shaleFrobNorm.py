import numpy as np
import csv
from csv import reader

def readfile(MZvalues, filename):
    '''
    :param MZvalues:
    :param filename:
    :return:
    '''
    count = 0
    frobzies = [0,0,0,0,0] #  Initialize list, each spot represents frobnorm of chem class
    with open(filename, 'r') as read_obj:
        #  read line by line so only one line is in memory at a time
        csv_reader = reader(read_obj)

        #  Loads a row from csv_reader one at a time
        for row in csv_reader:
            count +=1
            #  for each row, checks each chem class
            for i in range(len(MZvalues)):
                #  for each chem class, checks each m/z
                for x in MZvalues[i]:
                    if (row[x-30]) != '':  # -30 because the list index is shifted 30 down from actual m/z (42-30 = 12 as list index)
                        temp = int(float(row[(x-30)]))

                        if temp != 0:
                            if count > 94290:  # 15min into run, normalize for solv delay
                                frobzies[i] = frobzies[i] + (temp**2) # sums squares of m/z as it indexes
    for i in range(len(frobzies)):
        #  After getting each sum of squares, take sqrt to get frob norm
        frobzies[i] = np.sqrt(frobzies[i])
    print(count)
    return frobzies

def sort(frobenius, filename):
    '''
    :param frobenius:
    :param filename:
    :return:
    '''

    sorted = []  # container that holds sorted line to be appended to csv
    solvents = ['HexAc', 'TBaAc', 'Hexane', 'DCM', 'EA', 'TD', 'Tol']
    samples = ['1_1', '1_2', '1_3', '2_1', '2_2', '2_3', '3_1', '3_2', '3_3', '4_1', '4_2', '4_3', '5_1', '5_2', '5_3', '6_1', '6_2', '6_3', '7_1', '7_2', '7_3', 'QC', 'IBmid', 'IBend', 'TubeBlank', 'GWandSand', 'GW_tubeBlank']

    for item in solvents:
        if item in filename:
            sorted.append(item)
    for item in samples:
        if item in filename:
            sorted.append(item)
    for item in frobenius:
        sorted.append(item)
    writeline(sorted)

def writeheader():
    header = ['Solvent', 'Sample Number', 'Alkane', 'Cycloalkanes', 'Aromatics', 'Indanes', 'Naphthalenes']
    with open('Frobenius Norm Values.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header) # makes the csv with header

def writeline(frobenius):
    '''
    :param sorted_row:
    :param outputfilename:
    :return:
    '''
    with open('Frobenius Norm Values.csv', 'a', newline= '') as f:
        writer = csv.writer(f)
        writer.writerow(frobenius)

if __name__ == '__main__':

    # desired m/z values
    MZvalues = [[43, 57, 71, 85, 99], [41, 55, 69, 83, 97], [91, 105, 106, 119, 120, 134], [117, 118, 131, 132, 145, 146], [128, 141, 142, 155, 156, 170]]  # What m/z values you want
    # Alkanes, cycloalkanes, aromatics, indanes, naphthalenes [43, 57, 71, 85, 99], [41, 55, 69, 83, 97],
    # [91, 105, 106, 119, 120, 134], [117, 118, 131, 132, 145, 146], [128, 141, 142, 155, 156, 170]

    writeheader()   # makes csv w/ header
    #  opens text file containing filenames and runs in sequence
    with open('queue.txt', 'r') as read_obj:
        filename = read_obj.readline()
        while filename != '':
            filename = filename[:-1]  # takes off '\n' at end
            frobenius = readfile(MZvalues, filename)
            sort(frobenius, filename)
            filename = read_obj.readline()