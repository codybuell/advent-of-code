#!/usr/bin/env python3
# https://adventofcode.com/2024/day/2

import os

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# transform the data
runs = []
for line in lines:
    runs.append([int(x) for x in line.split(' ')])


def process_line(values):
    direction = ''

    safe = True
    for i in range(len(values) - 1):
        # get diff
        diff = values[i] - values[i + 1]

        # check level change
        if abs(diff) < 1 or abs(diff) > 3:
            safe = False
            break

        # check direction change
        if diff > 0:
            if direction == '':
                direction = 'decreasing'
                continue
            elif direction == 'increasing':
                safe = False
                break
        else:
            if direction == '':
                direction = 'increasing'
                continue
            elif direction == 'decreasing':
                safe = False
                break

    if safe:
        return True
    else:
        return False


invalid = 0
valid   = 0
states  = []
for run in runs:
    if process_line(run):
        valid += 1
        states.append("safe")
    else:
        invalid += 1
        states.append("unsafe")

print(valid)

for i in range(len(states)):
    if states[i] == 'unsafe':
        salvageable = False
        for j in range(len(runs[i])):
            newline = [item for k, item in enumerate(runs[i]) if k != j]
            if process_line(newline):
                salvageable = True
                break
        if salvageable:
            valid += 1

print(valid)
