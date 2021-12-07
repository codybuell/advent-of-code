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


##########
#  main  #
##########

if __name__ == "__main__":
    print('Part 1:', part1())
    print('Part 2:', part2())
