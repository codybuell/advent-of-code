#!/usr/bin/env python3
# https://adventofcode.com/2022/day/3

import os

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# transform
bags = [list(line) for line in lines]


def letter_to_score(letter: str) -> int:
    if letter.isupper():
        return ord(letter) - 38
    else:
        return ord(letter) - 96


# loop through bags
dupes = []
for bag in bags:
    length = int(len(bag) / 2)
    first  = bag[:length]
    second = bag[length:]
    dupes.append(list(set([x for x in first if x in second]))[0])

# loop through dupes
score = 0
for dupe in dupes:
    score += letter_to_score(dupe)

print('part 1:', score)

# put into groups of three
groups = [bags[i:i + 3] for i in range(0, len(bags), 3)]

# find badges and score
score = 0
for group in groups:
    badge = list(set([x for x in group[0] if x in group[1] and x in group[2]]))[0]
    score += letter_to_score(badge)

print('part 2:', score)
