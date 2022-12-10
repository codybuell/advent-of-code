#!/usr/bin/env python3
# https://adventofcode.com/2022/day/10

import os

# ingest data
data  = open(os.path.join(os.path.dirname(__file__), 'data.txt'), 'r')
lines = data.read().splitlines()

instructions = [line.split(' ') for line in lines]


def run(instructions: list):
    X = 1
    inst = 0
    cycle_on_inst = 0
    cycle = 0
    signal_strengths = []
    cycles = []

    while True:
        # check if we have reached the end of the instruction set
        if inst == len(instructions):
            break

        # grab the current operation
        instruction = instructions[inst][0]
        to_add = 0

        if instruction == 'noop':
            # handle a noop, increment instruction
            inst += 1
        else:
            if cycle_on_inst == 0:
                # handle first cycle of 2 cycle instruction
                cycle_on_inst += 1
            else:
                # handle second cycle of 2 cycle instruction
                cycle_on_inst = 0
                to_add = int(instructions[inst][1])
                inst += 1

        # print('cycle', cycle + 1, 'X =', X)
        cycles.append(X)

        cycle += 1

        if cycle == 20 or (cycle - 20) % 40 == 0:
            # print('SIGNAL_STRENGTH =', cycle * X)
            signal_strengths.append(cycle * X)

        X += to_add

    return sum(signal_strengths), cycles


sig_stren, cycles = run(instructions)
print('part 1:', sig_stren)


i = 0
screen = []
for x in range(6):
    screen.append([])
    for y in range(40):
        sprite_pos = cycles[i]
        sprite_range = [sprite_pos - 1, sprite_pos, sprite_pos + 1]
        if y in sprite_range:
            screen[x].append('#')
        else:
            screen[x].append('.')
        i += 1

print("part 2:")
for row in screen:
    print(''.join(row))
