#!/usr/bin/python
# -*- coding: utf-8 -*-

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])
    values = []
    weights = []
    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    items = len(values)

#dp algorithm:
    print items * capacity
    ltable = [ [] ]

    tuples = zip(values,weights)

    for j in range(0,items+1):
        ltable.append([])
        for k in range(0,capacity+1):
            ltable[j].append([])
            ltable[j][k] = ((0,0))


            if(j == 0 or k == 0):
                continue


            if(weights[j-1] <= k):
                ltable[j][k] = tuples[j-1]
            else:
                ltable[j][k] = ltable[j-1][k]
                continue


            if(weights[j-1] + ltable[j-1][k][1] <= k):
                ltable[j][k] = tuple(a+b for a,b in zip(ltable[j-1][k], tuples[j-1]))
            if(ltable[j-1][k][0] > values[j-1]):
                ltable[j][k] = ltable[j-1][k]


            if (ltable[j-1][k-weights[j-1]][0] + values[j-1] > ltable[j-1][k][0]):
                ltable[j][k] = tuple(a+b for a, b in zip(ltable[j-1][k-weights[j-1]], tuples[j-1]))
            else:
                ltable[j][k] = ltable[j-1][k]
        print "-",
    print "done"
        
    value =  ltable[items][capacity][0]
    print "backtracking..."
    taken = []
    i = items
    j = capacity
    for i in range(items,0,-1):
        if(ltable[i][j][0] == ltable[i-1][j][0]):
            taken.append(0)
        else:
            j = j - weights[i-1]
            taken.append(1)

    taken.reverse()


    for k in range(0,capacity+1):
        for j in range(0,items+1):
            print str(ltable[j][k][0]) + "\t",
        print ""
    
#    print table[(items,capacity,0)]        
    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(1) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

