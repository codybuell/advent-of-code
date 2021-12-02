#!/usr/bin/env python
# https://adventofcode.com/2021/day/2

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().splitlines()

# transform
instructions = []
for line in lines:
    i = line.split()
    instructions.append([i[0], int(i[1])])


###########
#  parts  #
###########


def part1():
    # depth, horizontal
    position = [0, 0]
    for i in instructions:
        if i[0] == 'forward':
            position[1] += i[1]
        elif i[0] == 'up':
            position[0] -= i[1]
        elif i[0] == 'down':
            position[0] += i[1]
    print(position)
    print(position[0] * position[1])


def part2():
    # depth, horizontal, aim
    position = [0, 0, 0]
    for i in instructions:
        if i[0] == 'forward':
            position[1] += i[1]
            position[0] += i[1] * position[2]
        elif i[0] == 'up':
            position[2] -= i[1]
        elif i[0] == 'down':
            position[2] += i[1]
    print(position)
    print(position[0] * position[1])


##########
#  main  #
##########


if __name__ == "__main__":
    part1()
    print('---')
    part2()
