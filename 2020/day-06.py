#!/usr/bin/env python3
# https://adventofcode.com/2020/day/6

import re

dataFile = open('day-06.txt', 'r')
groups   = dataFile.read().split('\n\n')

def part1():
    uniqueValues = []
    totalUniques = 0
    for group in groups:
        groupUniques = set(re.sub('\n', '', group))
        uniqueValues.append(groupUniques)
        totalUniques += len(groupUniques)

    print(totalUniques)
    return uniqueValues

def part2():
    totalUniques = 0
    for group in groups:
        groupList = [set(string) for string in group.splitlines()]
        intersection = set.intersection(*groupList)
        totalUniques += len(intersection)

    print(totalUniques)

if __name__ == "__main__":
    # total unique values by group
    part1()
    part2()
