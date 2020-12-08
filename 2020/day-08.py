#!/usr/bin/env python3
# https://adventofcode.com/2020/day/8

import re

dataFile = open('day-08.txt', 'r')
lines    = dataFile.read().splitlines()
length   = len(lines)

def part1(commands, position, accumulator=0, steps=0, visited=[]):
    if position == len(lines):
        print("booting complete on step " + str(steps) + " with acc of " + str(accumulator))
        return position
    p = re.compile('(^.*) (.*$)')
    m = re.match(p, commands[position])
    if m:
        a = m.group(1)
        v = m.group(2)

        steps += 1
        visited.append(position)

        if a == 'nop':
            position   += 1
        if a == 'acc':
            position   += 1
            accumulator = accumulator + eval(v)
        if a == 'jmp':
            position = position + eval(v)

        if position in visited:
            print("bailing on step " + str(steps) + " with acc of " + str(accumulator))
            return position

        position = part1(commands, position, accumulator, steps, visited)
        return position

def part2():
    for i in range(length):
        moddedLines = lines.copy()
        p = re.compile('(^.*) (.*$)')
        m = re.match(p, lines[i])
        if m:
            if m.group(1) == 'jmp':
                moddedLines[i] = re.sub('jmp', 'nop', lines[i])
            elif m.group(1) == 'nop':
                moddedLines[i] = re.sub('nop', 'jmp', lines[i])
            else:
                continue
            # visited param keeps value between func calls? have to set to empty array...
            endPosition = part1(moddedLines, 0, 0, 0, [])
            if endPosition == length:
                return

if __name__ == "__main__":
    part1(lines, 0)
    print('---')
    part2()
