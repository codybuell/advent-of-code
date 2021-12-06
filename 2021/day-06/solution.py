#!/usr/bin/env python
# https://adventofcode.com/2021/day/6

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
lines = dataFile.read().split(',')

# transform
fishes = [int(x) for x in lines]

###########
#  funcs  #
###########


def run_lanternfish(days: int, feesh: list) -> int:
    for day in range(days):
        to_append = 0
        for idx, fish in enumerate(feesh):
            if fish == 0:
                feesh[idx] = 6
                to_append += 1
            else:
                feesh[idx] -= 1

        feesh.extend([8] * to_append)

    return len(feesh)


def run_lanternfish_optimized(days: int, feesh: list) -> int:
    # instead of dealing with a every fish, lets group them by age and move
    # them in bulk, makes for dratically less crap to wade through
    the_feesh_registry = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # register our fishes
    for fish in feesh:
        the_feesh_registry[fish] += 1

    # run the simulation
    for day in range(days):
        zeros = the_feesh_registry.pop(0)
        the_feesh_registry[6] += zeros
        the_feesh_registry.append(zeros)

    sum = 0
    for fish in the_feesh_registry:
        sum += fish

    return(sum)


###########
#  parts  #
###########


def part1():
    school_one = fishes.copy()
    print(run_lanternfish(80, school_one))


def part2():
    school_two = fishes.copy()
    print(run_lanternfish_optimized(256, school_two))


##########
#  main  #
##########

if __name__ == "__main__":
    part1()
    print('---')
    part2()
