#!/usr/bin/env python3
# https://adventofcode.com/2023/day/6

import os
import re

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# break out times and distances for each race
race_lengths = [int(x) for x in re.sub(r'Time:\s+', '', lines[0]).split()]
distances   = [int(x) for x in re.sub(r'Distance:\s+', '', lines[1]).split()]

# dist = speed * duration
# duration = racelength(ms) - chargetime(ms)
# speed = 1mm/ms * chargetime(ms)

# dist = chargetime * (racelength - chargetime)

############
#  part 1  #
############


def part1_race(chargetime: int, race_length) -> int:
    return chargetime * (race_length - chargetime)


nums = []
for idx, race in enumerate(race_lengths):
    win = 0
    for chargetime in range(1, race):
        if part1_race(chargetime, race) > distances[idx]:
            win += 1
    nums.append(win)

total = 1
for num in nums:
    total *= num

print('Part 1:', total)

############
#  part 2  #
############

length = int(''.join([str(x) for x in race_lengths]))
distance = int(''.join([str(x) for x in distances]))

win = 0
for chargetime in range(1, length):
    if part1_race(chargetime, length) > distance:
        win += 1
nums.append(win)

print('Part 2:', win)
