#!/usr/bin/env python3
# https://adventofcode.com/2020/day/14

import re
import math
import sys

dataFile   = open('day-14.txt', 'r')
lines      = dataFile.read().splitlines()

def part1():
    p = re.compile('(^\S*) = (\S*$)')
    mem  = {}
    bmsk = 0
    for step in lines:
        m = re.match(p, step)
        lhs = m.group(1)
        val = m.group(2)
        if lhs == 'mask':
            # update our bitmask string
            bmsk = val
        else:
            # convert our value to an int for bitwise operations
            val = int(val)

            # run mask for 1's, convert all x's to 0's and run bitwise or
            val |= int(bmsk.replace('X','0'),2)

            # run mask for 0's, convert all x's to 1's and run bitwise and
            val &= int(bmsk.replace('X','1'),2)

            # append it to our dictionary
            exec(lhs + '=' + str(val))

    print(sum(mem.values()))

def part2():
    p = re.compile('(^\S*) = (\S*$)')
    mem  = {}
    bmsk = 0
    for step in lines:
        m = re.match(p, step)
        lhs = m.group(1)
        val = m.group(2)
        if lhs == 'mask':
            # update our bitmask string
            bmsk = val
        else:
            # init mem locations list
            locations = set()

            # parse our instruction line
            addr  = int(re.sub('[^\d]', '', lhs))
            value = int(val)

            # convert all X's to 0's and run bitwise or to process non X's in mask
            firstAddr = addr | int(bmsk.replace('X','0'),2)
            locations.add(firstAddr)

            # for each permutation of X's run an xor against the firstAddr
            xCount = bmsk.count('X')
            for i in range(1<<xCount):
                s = bin(i)[2:]
                s = '0' * (xCount - len(s)) + s
                # make a temp mask, replace all 1's with 0's for our xor operation
                tempmask = bmsk.replace('1', '0')
                # now replace our x's with this permutation
                for j in list(s):
                    tempmask = tempmask.replace('X', j, 1)
                # run our bitwise xor and add it to locations set
                locations.add(firstAddr ^ int(tempmask, 2))

            # write the value to each location
            for i in locations:
                mem[i] = value

    print(sum(mem.values()))

if __name__ == "__main__":
    part1()
    part2()
