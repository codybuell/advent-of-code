#!/usr/bin/env python3
# https://adventofcode.com/2023/day/4

import os
import re

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# build out our object
cards  = {}
pCard  = re.compile(r"Card\s+(\d+):\s+(.*)")
pGames = re.compile(r"([^\|]+)\s+\|\s+(\S.*)")
for line in lines:
    card = re.match(pCard, line)
    id   = card.group(1)
    nums = re.match(pGames, card.group(2))
    wins = [int(x) for x in nums.group(1).split()]
    have = [int(x) for x in nums.group(2).split()]
    cards[id] = {
        'wins': wins,
        'have': have,
        'copies': 1,
    }

# part 1
total = 0
for id, nums in cards.items():
    matches = len([x for x in nums['have'] if x in nums['wins']])
    total += (1 << matches - 1) if matches else 0

print('Part 1:', total)

# part 2
for id, nums in cards.items():
    matches = len([x for x in nums['have'] if x in nums['wins']])
    for x in range(matches):
        target = str(x + int(id) + 1)
        cards[target]['copies'] += nums['copies']

sum = 0
for id, nums in cards.items():
    sum += nums['copies']

print('Part 2:', sum)
