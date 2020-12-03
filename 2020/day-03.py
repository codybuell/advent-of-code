#!/usr/bin/env python3
# https://adventofcode.com/2020/day/3

import re

dataFile = open('day-03.txt', 'r')
lines = dataFile.read().splitlines()

def runtheslope(start,angle):
    patWidth = len(lines[0])
    yStep    = 0
    xStep    = 0
    hits     = 0
    i        = 0

    for line in lines:
        x = (xStep * angle[0]) % patWidth
        y = (yStep * angle[1]) 
        print(lines[i])
        if i == y:
            print(" " * x, end='')
            print("^", " " * (patWidth - x), "x=" + str(x), end='')
            xStep += 1
            yStep += 1
            spaceVal = lines[i][x]
            if spaceVal == "#":
                print(' hit')
                hits += 1
            else:
                print(' miss')
        else:
            print("--- skipping ---")
        i +=1

    print('--------------------------------------------------')
    return hits

def part1():
    start    = [0,0]
    angle    = [3,1]
    hits = runtheslope(start,angle)
    print(hits)

def part2():
    start    = [0,0]
    angle1   = [1,1]
    angle2   = [3,1]
    angle3   = [5,1]
    angle4   = [7,1]
    angle5   = [1,2]

    hits = []
    hits.append(runtheslope(start,angle1))
    hits.append(runtheslope(start,angle2))
    hits.append(runtheslope(start,angle3))
    hits.append(runtheslope(start,angle4))
    hits.append(runtheslope(start,angle5))

    print(hits)
    result = 1
    for x in hits:
         result = result * x
    print(result)

if __name__ == "__main__":
    part1()
    part2()
