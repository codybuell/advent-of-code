#!/usr/bin/env python3
# https://adventofcode.com/2022/day/1

import os

# ingest data
dataFile = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = dataFile.read().splitlines()

# transform into list of elves with lists of foods
elves = [[]]
elf = 0
for line in lines:
    if line != '':
        elves[elf].append(int(line))
    else:
        elves.append([])
        elf += 1

# build totals for each elf
totals = [sum(elf) for elf in elves]

# show the highest calorie caount
print('part 1:', max(totals))

# sort the totals descending
totals.sort(reverse=True)

# show total of top three elves calories
print('part 2:', sum(totals[:3]))
