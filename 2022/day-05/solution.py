#!/usr/bin/env python3
# https://adventofcode.com/2022/day/5

import os
import copy

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

# transform
line_break = lines.index('')
state = lines[:line_break]
instructions = lines[line_break + 1:]

# process state into stacks dict, reversed so we can pop/append
stack_labels  = state.pop()
stack_numbers = stack_labels.replace(' ', '')
state.reverse()
stacks = {}
for i in stack_numbers:
    index = stack_labels.index(i)
    stacks[i] = []
    for s in state:
        if len(s) > index and s[index] != ' ':
            stacks[i].append(s[index])

# run instructions (moves one crate at a time)
stacks_pt1 = copy.deepcopy(stacks)
for instruction in instructions:
    i = instruction.split(' ')
    amount = int(i[1])
    from_stack = i[3]
    to_stack = i[5]

    for _ in range(0, amount):
        item = stacks_pt1[from_stack].pop()
        stacks_pt1[to_stack].append(item)

result = ''.join([stacks_pt1[i][-1] for i in stacks_pt1])
print('part 1:', result)

# run new instructions (move all crates at once)
for instruction in instructions:
    i = instruction.split(' ')
    amount = int(i[1])
    from_stack = i[3]
    to_stack = i[5]

    moving = []
    for _ in range(0, amount):
        item = stacks[from_stack].pop()
        moving.append(item)

    moving.reverse()
    stacks[to_stack].extend(moving)

result = ''.join([stacks[i][-1] for i in stacks])
print('part 2:', result)
