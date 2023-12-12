#!/usr/bin/env python3
# https://adventofcode.com/2023/day/11

import os
import re

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# measure size
width  = len(lines[0])
height = len(lines)

# patterns (digits, symbols, gears)
pD = re.compile(r'\d+')
pS = re.compile(r'[^\d\.]')
pG = re.compile(r'\*')

to_sum = []
gears  = {}

for idx, line in enumerate(lines):
    for m in re.finditer(pD, line):
        # get start and end indexes and value
        s = m.start()
        e = m.end()
        n = int(line[s:e])

        # get surrounding coords
        checkL = max(0, s - 1)
        checkR = min(e + 1, width - 1)
        checkT = max(0, idx - 1)
        checkB = min(idx + 1, height - 1)

        # grab surrounding chunks
        above  = '' if checkT == idx else lines[checkT][checkL:checkR]
        below  = '' if checkB == idx else lines[checkB][checkL:checkR]
        front  = '' if checkL == s else line[checkL]
        behind = '' if checkR == e - 1 else line[e]

        # check for any possible 'gears'
        for g in re.finditer(pG, above):
            x = g.start() + checkL
            y = checkT
            gears.setdefault((x, y), []).append(n)

        for g in re.finditer(pG, below):
            x = g.start() + checkL
            y = checkB
            gears.setdefault((x, y), []).append(n)

        if '*' in front:
            x = checkL
            y = idx
            gears.setdefault((x, y), []).append(n)

        if '*' in behind:
            x = checkR - 1
            y = idx
            gears.setdefault((x, y), []).append(n)

        # look for any non digit or non .
        combined = above + below + front + behind
        m = re.search(pS, combined)
        if m:
            to_sum.append(n)

# sum up gear ratios
total = 0
for _, parts in gears.items():
    if len(parts) == 2:
        total += parts[0] * parts[1]

print('Part 1:', sum(to_sum))
print('Part 2:', total)
