#!/usr/bin/env python3
# https://adventofcode.com/2020/day/10

import re

dataFile   = open('day-10.txt', 'r')
lines      = [int(x) for x in dataFile.read().splitlines()]
maxJoltGap = 3

def part1():
    # start is 0 jolts
    # count of 3 jolt differences is always 1
    # start by sorting adapter sizes low to high
    # for each value diff it +1 index and append to diff list
    # total 1 diffs and 3 diffs
    lines.sort()
    lines.insert(0, 0)
    length = len(lines)
    diffs = []
    for idx, i in enumerate(lines):
        if (length - 1) == idx:
            diff = 3
        else:
            diff = lines[idx+1] - i
        diffs.append(diff)

    diffs1 = diffs.count(1)
    diffs3 = diffs.count(3)
    print("1 diffs: " + str(diffs1))
    print("3 diffs: " + str(diffs3))
    print("factored: " + str(diffs1 * diffs3))
    return diffs

def part2(diffs):
    # from our diffs sequence:
    # can never remove 3's
    # can never remove the last 1 in a sequence of 1's
    # bcs of jolt diff limit of 3, possibilities are reduced when we hit a sequence of ones >= 4
    # since adapter is there or not, probability is 2^(removable adapters) in a sequence, multiply all sequence possibilities
    # eg sequnces
    # 1     -> 2^0 = 1, last 1 in a seq is not avail
    # 11    -> 2^1 = 2, ""
    # 111   -> 2^2 = 4, ""
    # 1111  -> 2^3 = 8, "", but now we are hitting jolt limitations, which reduces by max(0,num of adapters in seq - max jolt gap)
    # 11111 -> 2^4 = 16, ""

    # moosh diff list together
    diffString = [str(x) for x in diffs]
    diffJoined = "".join(diffString)

    # split on 3's
    patterns = diffJoined.split('3')
    
    total = 1
    for i in patterns:
        numOfOnes = len(i)
        # ignore non sequnces and sequences of 1 as they provide no variants
        if numOfOnes > 1:
            total *= ((2 ** (numOfOnes - 1)) - max(0, numOfOnes - maxJoltGap))

    print(total)
    
if __name__ == "__main__":
    diffs = part1()
    part2(diffs)
