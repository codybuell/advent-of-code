#!/usr/bin/env python
# https://adventofcode.com/2021/day/1

###########
#  setup  #
###########


dataFile = open('day-01.txt', 'r')
lines = dataFile.read().splitlines()
lines = [int(i) for i in lines]

#############
#  helpers  #
#############

def sum_three_positions(pos: int) -> int:
    # check next three positions exist
    if pos + 2 > len(lines) - 1:
        return

    # add up three positions starting with pos
    sum = 0
    for i in range(3):
        loc = pos + i
        sum += lines[loc]

    return sum

###########
#  parts  #
###########

def part1():
    increased = 0
    for line in range(len(lines)):
        if line == 0:
            continue
        last_line = line - 1
        if lines[line] > lines[last_line]:
            increased += 1
    print(increased)

def part2():
    increased = 0
    for line in range(len(lines)):
        sumone = sum_three_positions(line)
        sumtwo = sum_three_positions(line + 1)
        if sumone is not None and sumtwo is not None:
            if sumtwo > sumone:
                increased += 1
    print(increased)

##########
#  main  #
##########

if __name__ == "__main__":
    part1()
    print('---')
    part2()
