#!/usr/bin/env python
# https://adventofcode.com/2021/day/7

###########
#  setup  #
###########


# ingest data
dataFile = open('data.txt', 'r')
crab_subs = dataFile.read().split(',')

# transform
crab_subs = [int(x) for x in crab_subs]

###########
#  funcs  #
###########


def sumorial(num: int) -> int:
    # aka summation / n-th triangular number / terminal function
    return (num * (num + 1)) // 2


###########
#  parts  #
###########


def part1():
    winning_position = 9999999
    winning_pos_fuel = 9999999
    for position in range(max(crab_subs) + 1):
        fuel_spent = 0
        for crab_pos in crab_subs:
            fuel_to_move = abs(crab_pos - position)
            fuel_spent += fuel_to_move
        if fuel_spent < winning_pos_fuel:
            winning_position = position
            winning_pos_fuel = fuel_spent

    return (winning_position, winning_pos_fuel)


def part2():
    winning_position = 99999999999
    winning_pos_fuel = 99999999999
    for position in range(max(crab_subs) + 1):
        fuel_spent = 0
        for crab_pos in crab_subs:
            fuel_cost = 1
            fuel_to_move = 0
            for move in range(abs(crab_pos - position)):
                fuel_to_move += fuel_cost + move
            fuel_spent += fuel_to_move
        if fuel_spent < winning_pos_fuel:
            winning_position = position
            winning_pos_fuel = fuel_spent

    return (winning_position, winning_pos_fuel)


def part1_median_method():
    # get the median (middle number in list)
    sorted_copy = crab_subs.copy()
    sorted_copy.sort()
    if (len(sorted_copy) % 2) == 0:
        # we don't have a middle number so we need to average the two around the center
        lower = int(len(sorted_copy) / 2)
        upper = lower + 1
        median = (sorted_copy[lower] + sorted_copy[upper]) / 2
    else:
        median = sorted_copy[int(len(sorted_copy))]

    # find amount of fuel spent for each sub to get to median
    fuel_spent = 0
    for i in crab_subs:
        fuel_spent += abs(median - i)

    return(int(median), int(fuel_spent))


def part2_mean_method():
    # get mean (average of numbers in list)
    total = 0
    for i in crab_subs:
        total += i
    avg = int(total / len(crab_subs))

    fuel_spent = 0
    for i in crab_subs:
        # sumorial the difference between current pos and target (avg)
        fuel_spent += sumorial(abs(avg - i))
        # alt method using sum() and range()
        # fuel_spent += sum(range(abs(avg - i) + 1))

    return(avg, int(fuel_spent))


##########
#  main  #
##########
if __name__ == "__main__":
    # brute force (1 min on m1 mac)
    # print('Part 1:', part1())
    # print('Part 2:', part2())

    # smart way ()
    print('Part 1:', part1_median_method())
    print('Part 2:', part2_mean_method())
