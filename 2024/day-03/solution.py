#!/usr/bin/env python3
# https://adventofcode.com/2024/day/3

import os
import re

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# part 1
funcs = re.compile(r'mul\((\d+),(\d+)\)')

sum = 0
for line in lines:
    matches = re.finditer(funcs, line)
    for match in matches:
        sum += int(match.group(1)) * int(match.group(2))

print(sum)

# part 2
pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")

sum = 0
add = True
for line in lines:
    matches = re.finditer(pattern, line)
    execute_instr = []
    for match in matches:
        print(match.group())
        if match.group() == "do()":
            add = True
        elif match.group() == "don't()":
            add = False
        elif add:
            sum += int(match.group(1)) * int(match.group(2))

print(sum)
