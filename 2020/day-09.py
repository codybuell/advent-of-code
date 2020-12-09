#!/usr/bin/env python3
# https://adventofcode.com/2020/day/9

import re

dataFile = open('day-09.txt', 'r')
lines    = [int(x) for x in dataFile.read().splitlines()]

def part1(preamble_size):
    for i in range(len(lines)):
        preamble = lines[i:(preamble_size + i)]
        target   = lines[preamble_size + i]
        valid    = False
        for idxj, j in enumerate(preamble):
            for idxk, k in enumerate(preamble[idxj:]):
                idxk += idxj
                if idxj == idxk:
                    continue
                if (j + k) == target:
                    valid = True
        if not valid:
            print(target)
            return target

def part2(target):
    found = False
    for idx, i in enumerate(lines):
        length  = len(lines) - idx
        total   = i
        summing = [i]
        for i in range(length):
            nextint = lines[i + 1 + idx]
            summing.append(nextint)
            total += nextint
            # print("target: " + str(target))
            # print("summing: ", end='')
            # print(summing)
            # print("total: " + str(total))
            if total < target:
                continue
            if total > target:
                break
            if total == target:
                weakness = min(summing) + max(summing)
                print(weakness)
                found = True
                break
        if found:
            break

if __name__ == "__main__":
    target = part1(25)
    part2(target)
