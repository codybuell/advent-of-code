#!/usr/bin/env python3
# https://adventofcode.com/2022/day/4

import os

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# transform
pairs = [[[int(y) for y in x.split('-')] for x in line.split(',')] for line in lines]

contained = 0
for pair in pairs:
    first  = pair[0]
    second = pair[1]

    if first[0] >= second[0] and first[1] <= second[1]:
        contained += 1
        continue

    if second[0] >= first[0] and second[1] <= first[1]:
        contained += 1
        continue


print('part 1:', contained)

overlapped = 0
for pair in pairs:
    first  = pair[0]
    second = pair[1]

    if first[0] >= second[0] and first[0] <= second[1]:
        overlapped += 1
        continue

    if second[0] >= first[0] and second[0] <= first[1]:
        overlapped += 1
        continue

print('part 2:', overlapped)
