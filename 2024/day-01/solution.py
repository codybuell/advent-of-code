#!/usr/bin/env python3
# https://adventofcode.com/2024/day/1

import os
import re

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

left = []
right = []

for line in lines:
    split = re.split(r'\s+', line)
    left.append(int(split[0]))
    right.append(int(split[1]))

left = sorted(left)
right = sorted(right)

diffs = []
for i in range(len(left)):
    items = [left[i], right[i]]
    diffs.append(max(items) - min(items))

print(sum(diff for diff in diffs))

total = 0
for i in left:
    count = right.count(i)
    total += i * count

print(total)
