#!/usr/bin/env python3
# https://adventofcode.com/2020/day/5

import re

dataFile = open('day-05.txt', 'r')
passes   = dataFile.read().splitlines()

def parseVal(seatCode, values):
    val = [*range(values)]
    for i in range(len(seatCode)):
        mid = len(val) // 2
        if re.match('(F|L)', seatCode[i]) is not None:
            val = val[:mid]
        if re.match('(B|R)', seatCode[i]) is not None:
            val = val[mid:]
    return val[0]

def parseID(row, col):
    return (row * 8) + col

def part1():
    seatIDs = []
    for seat in passes:
        row = parseVal(seat[:7], 128)
        col = parseVal(seat[7:], 8)
        idd = parseID(row, col)
        seatIDs.append(idd)

    print(max(seatIDs))
    return seatIDs

def part2(seatIDs):
    seatIDs.sort()
    for i in seatIDs:
        if (seatIDs[i] + 1) != (seatIDs[i+1]):
            print(seatIDs[i] + 1)
            return seatIDs[i] + 1

if __name__ == "__main__":
    ids = part1()
    part2(ids)
