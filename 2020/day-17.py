#!/usr/bin/env python3
# https://adventofcode.com/2020/day/17

import re
import sys
import copy
import itertools

dataFile    = open('day-17.txt', 'r')
init_matrix = [[list(x) for x in dataFile.read().splitlines()]]

def print_matrix(matrix):
    for z in matrix:
        for y in z:
            print(y)
        print('-' * len(matrix[0][0] * 5))

def grow_matrix(matrix):
    # grow x and y dimiensions on each z
    for idxz, z in enumerate(matrix):
        for idxy, y in enumerate(z):
            y.insert(0,'.')
            y.append('.')
        blank = [x.replace('#','.') for x in z[0].copy()]
        z.insert(0, blank)
        z.append(blank.copy())

    # grow in z
    layer = copy.deepcopy(matrix[0])
    for idxy, y in enumerate(layer):
        layer[idxy] = [x.replace('#','.') for x in y]
    matrix.insert(0, layer)
    matrix.append(copy.deepcopy(layer))

    return matrix

def cubesAround(cube, matrix):
    # cube -> [z,y,x]
    # matrix[z][y][x], determine dimensions
    zRange = len(matrix) - 1
    yRange = len(matrix[0]) - 1
    xRange = len(matrix[0][0]) - 1

    # range to check around
    checkRange = range(-1,2)

    # build a list of all locations around seat, account for edge limits on z, y, and x dimensions
    aroundCoords = [[min(zRange, max(0,cube[0] + z)), min(yRange, max(0,cube[1] + y)), min(xRange, max(0,cube[2] + x))] for z in checkRange for y in checkRange for x in checkRange]

    # remove duplicates from list
    aroundCoords.sort()
    aroundCoords = [aroundCoords for aroundCoords,_ in itertools.groupby(aroundCoords)]

    # remove the cube itself
    aroundCoords.remove(cube)

    # get values of those locations
    aroundValues = [matrix[i[0]][i[1]][i[2]] for i in aroundCoords]

    return aroundCoords, aroundValues

def grow_hyper_matrix(matrix):
    # grow x and y dimiensions on all z and w
    for w in matrix:
        for z in w:
            for y in z:
                y.insert(0,'.')
                y.append('.')
            blank = [x.replace('#','.') for x in z[0].copy()]
            z.insert(0, blank)
            z.append(blank.copy())

    # make a fresh z layer
    layer = copy.deepcopy(matrix[0][0])
    for idxy, y in enumerate(layer):
        layer[idxy] = [x.replace('#','.') for x in y]

    # grow z on all w
    for w in matrix:
        w.insert(0, copy.deepcopy(layer))
        w.append(copy.deepcopy(layer))

    # grow in z
    zslice = copy.deepcopy(matrix[0])
    for idxz, z in enumerate(zslice):
        for idxy, y in enumerate(z):
            zslice[idxz][idxy] = [x.replace('#','.') for x in y]
    matrix.insert(0, zslice)
    matrix.append(copy.deepcopy(zslice))

    return matrix

def hyperAround(hypercube, matrix):
    # hypercube -> [w,z,y,x]
    # matrix[w][z][y][x], determine dimensions
    wRange = len(matrix) - 1
    zRange = len(matrix[0]) - 1
    yRange = len(matrix[0][0]) - 1
    xRange = len(matrix[0][0][0]) - 1

    # range to check around
    checkRange = range(-1,2)

    # build a list of all locations around seat, account for edge limits on z, y, and x dimensions
    aroundCoords = [[min(wRange, max(0,hypercube[0] + w)), min(zRange, max(0,hypercube[1] + z)), min(yRange, max(0,hypercube[2] + y)), min(xRange, max(0,hypercube[3] + x))] for w in checkRange for z in checkRange for y in checkRange for x in checkRange]

    # remove duplicates from list
    aroundCoords.sort()
    aroundCoords = [aroundCoords for aroundCoords,_ in itertools.groupby(aroundCoords)]

    # remove the hypercube itself
    aroundCoords.remove(hypercube)

    # get values of those locations
    aroundValues = [matrix[i[0]][i[1]][i[2]][i[3]] for i in aroundCoords]

    return aroundCoords, aroundValues

def part1(matrix, target_cycles, steps=0):
    # check if we are done
    if steps == target_cycles:
        count = 0
        for z in matrix:
            for y in z:
                count += y.count('#')
        print(count)
        return

    # prepare next generation matrix to store changes, takes
    # current matrix and grows an inactive shell around each dimension
    # making a copy otherwise changes will modify current generation
    grow_matrix(matrix)
    nextMatrix = copy.deepcopy(matrix)

    # run life
    for idxz, z in enumerate(matrix):
        for idxy, y in enumerate(z):
            for idxx, x in enumerate(y):
                aroundCoords, aroundValues = cubesAround([idxz,idxy,idxx], matrix)
                if x == '#':
                    if aroundValues.count('#') not in range(2,4):
                        nextMatrix[idxz][idxy][idxx] = '.'
                else:
                    if aroundValues.count('#') == 3:
                        nextMatrix[idxz][idxy][idxx] = '#'

    # loop
    part1(nextMatrix, target_cycles, steps+1)

def part2(matrix, target_cycles, steps=0):
    # check if we are done
    if steps == target_cycles:
        count = 0
        for w in matrix:
            for z in w:
                for y in z:
                    count += y.count('#')
        print(count)
        return

    # prepare next generation matrix to store changes, takes
    # current matrix and grows an inactive shell around each dimension
    # making a copy otherwise changes will modify current generation
    grow_hyper_matrix(matrix)
    nextMatrix = copy.deepcopy(matrix)

    # print_matrix(matrix)
    # sys.exit(1)

    # run life
    for idxw, w in enumerate(matrix):
        for idxz, z in enumerate(w):
            for idxy, y in enumerate(z):
                for idxx, x in enumerate(y):
                    aroundCoords, aroundValues = hyperAround([idxw,idxz,idxy,idxx], matrix)
                    if x == '#':
                        if aroundValues.count('#') not in range(2,4):
                            nextMatrix[idxw][idxz][idxy][idxx] = '.'
                    else:
                        if aroundValues.count('#') == 3:
                            nextMatrix[idxw][idxz][idxy][idxx] = '#'

    # loop
    part2(nextMatrix, target_cycles, steps+1)

if __name__ == "__main__":
    part1(copy.deepcopy(init_matrix), 6)
    # our init matrix is only 3 dimensions, wrap in another when passing to part2
    part2([copy.deepcopy(init_matrix)], 6)
