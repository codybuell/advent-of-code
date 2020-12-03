#!/usr/bin/env python
# https://adventofcode.com/2020/day/2

import re

dataFile = open('day-02.txt', 'r')
lines = dataFile.read().splitlines()

def part1():
    validCount = 0
    invalidCount = 0
    for x in lines:
        # parse our line
        lowRange  = re.search("(^[0-9]+)-[0-9]+\s", x).group(1)
        highRange = re.search("^[0-9]+-([0-9]+)\s", x).group(1)
        charValue = re.search("\s(.):\s", x).group(1)
        pwdString = re.search(":\s(.*$)", x).group(1)
        # search for our required character
        instances = re.findall(charValue, pwdString)
        if len(instances) in range(int(lowRange), int(highRange) + 1):
            validCount += 1
        else:
            invalidCount += 1
    print(validCount)

def part2():
    validCount = 0
    invalidCount = 0
    for x in lines:
        # parse our line
        lowPos    = int(re.search("(^[0-9]+)-[0-9]+\s", x).group(1))
        highPos   = int(re.search("^[0-9]+-([0-9]+)\s", x).group(1))
        charValue = re.search("\s(.):\s", x).group(1)
        pwdString = re.search(":\s(.*$)", x).group(1)

        values = []

        if lowPos <= len(pwdString):
            values.append(pwdString[lowPos - 1])

        if highPos <= len(pwdString):
            values.append(pwdString[highPos - 1])

        matchstring = ""
        for i in range(highPos):
            if i == (lowPos - 1) or i == (highPos -1):
                matchstring += '^'
            else:
                matchstring += '-'

        print(pwdString)
        print(matchstring + " " + charValue)

        if values.count(charValue) == 1:
            validCount += 1
        else:
            invalidCount += 1

        print(values)

    print(validCount)

if __name__ == "__main__":
    part1()
    part2()
