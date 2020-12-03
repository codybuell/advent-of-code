#!/usr/bin/env python
# https://adventofcode.com/2020/day/1

dataFile = open('day-01.txt', 'r')
lines = dataFile.read().splitlines()

def part1():
    for x in lines:
        for y in lines:
            sumXY = int(x) + int(y)
            if int(sumXY) == 2020:
                factorXY = int(x) * int(y)
                print ' & '.join([x, y])
                print(factorXY)
                return

def part2():
    for x in lines:
        for y in lines:
            for z in lines:
                sumXYZ = int(x) + int(y) + int(z)
                if int(sumXYZ) == 2020:
                    factorXYZ = int(x) * int(y) * int(z)
                    print ' & '.join([x, y, z])
                    print(factorXYZ)
                    return
            
if __name__ == "__main__":
    part1()
    part2()
