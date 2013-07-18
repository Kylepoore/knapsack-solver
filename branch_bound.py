#!/usr/bin/python
# -*- coding: utf-8 -*-
best_estmate = 0
solutions = []
solution_values = []
best_complete_value = 0
best_complete_solution = []
low_bound = 0
values = []
weights = []

density = []

import math
def do_estimate(items,capacity,start):
    global low_bound
    global density
    global values
    global weights
    weight = 0
    valsum = 0
    index = 0
    priority = sorted(density[start:], reverse=True)
    fits = 1
#    for i in range(start,items):
#        (d, index) = priority[i-start]
    for d, index in priority:

        if (weight + weights[index][1] > capacity):
            fits = 0
            break
        else:
            weight += weights[index][1]
            valsum += values[index][1]
    fraction = 0
    left_over = 0
    if(start == 0):
        low_bound = valsum
    if(fits == 1):
        return valsum
    else:
        left_over = capacity - weight
        fraction = float(left_over) / float(weights[index][1])
    return int(valsum + (fraction * values[index][1]))
    

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])
    global original_capacity
    original_capacity = capacity
    global values
    global weights
    original_values = []
    original_weights = []
    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()
        original_values.append(int(parts[0]))
        original_weights.append(int(parts[1]))
        values.append((int(parts[0])/int(parts[1]),int(parts[0]),i-1))
        weights.append((int(parts[0])/int(parts[1]),int(parts[1]),i-1))


    values = sorted(values)
    values.reverse()
    weights = sorted(weights)
    weights.reverse()
    items = len(values)

    global density
    for i in range(items):
        density.append((float(values[i][1])/float(weights[i][1]),i))


    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = []
    global best_estimate
    best_estimate = do_estimate(items,capacity,0)
#    for i in range(0, items):
#        if weight + weights[i] <= capacity:
#            taken.append(1)
#            value += values[i]
#            weight += weights[i]
#        else:
#            taken.append(0)
    emptylist = []
    global best_complete_value
    global low_bound
    stack = [(1,best_estimate,capacity,value,emptylist)]
    while len(stack) > 0:
        (depth,estimate,cap,val,sol) = stack.pop()
        if(cap < 0): continue
        if(estimate <= best_complete_value): continue
        if(estimate < low_bound): continue
#        print depth
        if(val >= low_bound):
            low_bound = val
        if(len(sol) == items):
            if val > best_complete_value:
                best_complete_value = val
                best_complete_solution = sol
            continue
#        if(cap < 0):
#            print str(depth) + "\t" + str(estimate) + "\t" + str(best_complete_value) + "\t" + str(sol) + "**too heavy**\r"
#            continue
#        if(estimate <= best_complete_value):
#            print str(depth) + "\t" + str(estimate) + "\t" + str(best_complete_value) + "\t" + str(sol) + "**sub-optimal**\r"
#            continue
#        if(estimate < low_bound):
#            print str(depth) + "\t" + str(estimate) + "\t" + str(best_complete_value) + "\t" + str(sol) + "**sub-optimal**\r"
#            continue
#        print str(depth) + "\t" + str(estimate) + "\t" + str(best_complete_value) + "\t" + str(sol) + "\r"
        new_est = do_estimate(items,cap,depth)
#        if(new_est + val >= best_complete_value and new_est + val > low_bound):
        leave = list(sol)
        leave.append(0)
        stack.append((depth+1,new_est + val,cap,val,leave))
#        if(cap - weights[depth-1][1] >= 0):
        take = list(sol)
        take.append(1)
#        stack.append((depth+1,new_est + val + values[depth-1][1],cap - weights[depth-1][1],val + values[depth-1][1],take))
        stack.append((depth+1,estimate,cap - weights[depth-1][1],val + values[depth-1][1],take))

    taken = []
    value = best_complete_value
    best_solution = best_complete_solution
    indeces = []
    for i in range(0,items):
        index = 0
        (m,v,index) = values[i]
        indeces.append((index,i))
        #takenvalues[i][2]-1] = best_solution[i]
#    taken = solutions[solution_values.index(value)]
    sorted_indeces = sorted(indeces)
    total_weight = 0
    total_value = 0
    selected_weights = []
    for i in range(0,items):
        (a,b) = sorted_indeces[i]
        taken.append(best_complete_solution[b])
#        total_weight += best_complete_solution[b] * weights[b][1]
        total_value += best_complete_solution[b] * original_values[i]
#        selected_weights.append(best_complete_solution[b] * weights[b][1])
#    print total_value
#    print total_weight
#    print selected_weights
#    print original_weights
#    print sum(selected_weights)
#    print capacity
            
    # prepare the solution in the specified output format
    outputData = str(total_value) + ' ' + str(0) + '\n'
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

